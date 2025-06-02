```python
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_cylinder(ax, center, radius, height, color, resolution=50):
    """Dibuja un cilindro sólido"""
    x, y, z = center
    theta = np.linspace(0, 2*np.pi, resolution)
    z_grid = np.linspace(z, z + height, 2)
    theta_grid, z_grid = np.meshgrid(theta, z_grid)
    
    ax.plot_surface(
        radius * np.cos(theta_grid) + x,
        radius * np.sin(theta_grid) + y,
        z_grid,
        color=color
    )
    
    # Tapas
    for h in [z, z + height]:
        circle = np.array([radius * np.cos(theta) + x, 
                          radius * np.sin(theta) + y, 
                          np.full_like(theta, h)]).T
        ax.add_collection3d(Poly3DCollection([circle], color=color))

def draw_cube(ax, center, size, height, color):
    """Dibuja un prisma cuadrado (cubo)"""
    x, y, z = center
    half = size / 2
    vertices = [
        [x-half, y-half, z], [x+half, y-half, z], [x+half, y+half, z], [x-half, y+half, z],
        [x-half, y-half, z+height], [x+half, y-half, z+height], [x+half, y+half, z+height], [x-half, y+half, z+height]
    ]
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Base inferior
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Base superior
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Lado X+
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Lado X-
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Lado Y+
        [vertices[0], vertices[3], vertices[7], vertices[4]]   # Lado Y-
    ]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=0.5, edgecolors='k'))

def draw_hollow_cylinder(ax, center, r_outer, r_inner, height, color, resolution=50):
    """Dibuja un cilindro hueco (tipo dona)"""
    x, y, z = center
    theta = np.linspace(0, 2 * np.pi, resolution)
    z_vals = np.linspace(z, z + height, 2)
    theta_grid, z_grid = np.meshgrid(theta, z_vals)

    # Pared exterior
    x_outer = r_outer * np.cos(theta_grid) + x
    y_outer = r_outer * np.sin(theta_grid) + y
    ax.plot_surface(x_outer, y_outer, z_grid, color=color)

    # Pared interior
    x_inner = r_inner * np.cos(theta_grid) + x
    y_inner = r_inner * np.sin(theta_grid) + y
    ax.plot_surface(x_inner, y_inner, z_grid, color=color)

    # Tapa superior (anillo)
    top_outer = np.array([r_outer * np.cos(theta) + x, r_outer * np.sin(theta) + y, np.full_like(theta, z + height)]).T
    top_inner = np.array([r_inner * np.cos(theta) + x, r_inner * np.sin(theta) + y, np.full_like(theta, z + height)]).T
    top_ring = np.concatenate([top_outer, top_inner[::-1]])  # Sentido inverso para cerrar el anillo
    ax.add_collection3d(Poly3DCollection([top_ring], color=color))

# Configuración
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Colores
green = '#1AA032'
brown = '#8B4513'

# 1. Base cuadrada (color café)
draw_cube(ax, center=(0, 0, 0), size=2.8, height=0.3, color=brown)

# 2. Cilindro central (verde)
draw_cylinder(ax, center=(0, 0, 0.3), radius=1, height=2, color=green)

# 3. Cilindro superior hueco (verde tipo dona)
draw_hollow_cylinder(ax, center=(0, 0, 2.3), r_outer=1.3, r_inner=0.9, height=0.5, color=green)

# Ajustes visuales
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([0, 3])
ax.axis('off')
ax.view_init(elev=25, azim=30)
plt.tight_layout()
plt.show()

#AVANCE
```
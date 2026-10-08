import math

# Parameters
num_points = 13
radius = 0.3
center_x = 0.3
center_y = 0
elements = []

# Generate arch points from left to right (semi-circle)
arch_points = []
for i in range(num_points):
    theta = math.pi * i / (num_points - 1)  # angles from 0 to π
    x = center_x + radius * math.cos(theta)
    y = center_y + radius * math.sin(theta)
    arch_points.append([x, y])

# Radial spokes from arch to bottom center
for pt in arch_points:
    elements.append([pt, [center_x, center_y]])

# Top arch segments
for i in range(len(arch_points) - 1):
    elements.append([arch_points[i], arch_points[i + 1]])

# Final structure
bridge_structure = {
    "base": [[0, 0], [0.6, 0]],
    "subdivision": num_points - 1,
    "elements": elements
}

print(bridge_structure)
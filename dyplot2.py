
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import sobel

def generate_dots(image_path, num_dots=10000, edge_weight=2.0):
    img = Image.open(image_path)c
    # flip the image vertically
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    width, height = img.size
    aspect_ratio = height / width
    
    # Maintain aspect ratio while scaling
    target_width = 200
    target_height = int(target_width * aspect_ratio)
    img = img.resize((target_width, target_height))
    img_array = np.array(img) / 255.0
    
    # Calculate edges
    edge_x = sobel(img_array, axis=0)
    edge_y = sobel(img_array, axis=1)
    edges = np.sqrt(edge_x**2 + edge_y**2)
    
    # Combine intensity and edges for probability map
    prob_map = (1 - img_array) + (edge_weight * edges)
    prob_map = prob_map / prob_map.sum()
    
    # Generate continuous random points
    points = np.random.uniform(
        low=[0, 0],
        high=[target_width, target_height],
        size=(num_dots * 2, 2)  # Generate extra points for jittering
    )
    
    # Filter points based on probability map
    probs = prob_map[np.clip(points[:, 1].astype(int), 0, target_height-1),
                    np.clip(points[:, 0].astype(int), 0, target_width-1)]
    mask = np.random.random(len(points)) < probs/probs.max()
    points = points[mask][:num_dots]  # Take only needed number of points
    
    return points

def plot_dots(points, output_path=None):
    plt.figure(figsize=(10, 10), facecolor='white')
    plt.scatter(points[:, 0], points[:, 1], s=1, c='black', alpha=0.5)
    plt.axis('equal')
    plt.axis('off')
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor='white')
    plt.show()

import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

def generate_natural_curves(points, num_curves=100, points_per_curve=50):
    curves = []
    kdtree = KDTree(points)
    
    for _ in range(num_curves):
        start_idx = np.random.randint(len(points))
        current_point = points[start_idx]
        curve = [current_point]
        momentum = np.array([0., 0.])
        
        for _ in range(points_per_curve):
            indices = kdtree.query_ball_point(current_point, r=20)
            if len(indices) < 2:
                break
                
            candidates = points[indices]
            directions = candidates - current_point
            
            # Normalize directions and handle zero vectors
            dir_norms = np.linalg.norm(directions, axis=1)
            valid_dirs = dir_norms > 0
            if not np.any(valid_dirs):
                break
                
            directions = directions[valid_dirs]
            dir_norms = dir_norms[valid_dirs]
            
            # Calculate weights based on direction and current momentum
            weights = np.ones(len(directions))
            if np.any(momentum):
                mom_norm = np.linalg.norm(momentum)
                if mom_norm > 0:
                    alignment = np.dot(directions, momentum) / (dir_norms * mom_norm)
                    weights = np.exp(alignment) + 0.1
            
            weights /= weights.sum()
            
            # Select next point from valid candidates
            next_idx = np.random.choice(len(directions), p=weights)
            next_point = candidates[valid_dirs][next_idx]
            
            # Update momentum and add tremor
            momentum = 0.8 * momentum + 0.2 * (next_point - current_point)
            momentum += np.random.normal(0, 0.5, 2)
            
            # Generate curve segment with tremor
            tremor = np.random.normal(0, 0.3, (points_per_curve, 2))
            segment = np.linspace(current_point, next_point, points_per_curve) + tremor
            curves.append(segment)
            
            current_point = next_point
            
    return curves

def plot_curves(curves, points=None):
    plt.figure(figsize=(10, 10), facecolor='white')
    
    if points is not None:
        plt.scatter(points[:, 0], points[:, 1], s=1, c='red', alpha=0.1)
        
    for curve in curves:
        plt.plot(curve[:, 0], curve[:, 1], 'k-', linewidth=0.3, alpha=0.5)
    
    plt.axis('equal')
    plt.axis('off')
    plt.show()

# Example usage with previous dot generator:
points = generate_dots('image4.png', num_dots=100000, edge_weight=0.0)
curves = generate_natural_curves(points, num_curves=8000, points_per_curve=5)
plot_curves(curves)
# points = generate_dots('image2.png', num_dots=100000, edge_weight=2.0)
# plot_dots(points, 'output2.png')
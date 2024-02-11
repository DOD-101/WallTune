import os

original_path = "./hello/this/world"
# Normalize the path to ensure it uses the correct path separators for the current OS
normalized_path = os.path.normpath(original_path)
# Split the path into components
path_components = normalized_path.split(os.sep)
# Remove the unwanted parts
cutoff_index = path_components.index("hello") + 1
if cutoff_index > 0 and cutoff_index < len(path_components):
    del path_components[:cutoff_index]
# Reconstruct the path
modified_path = os.sep.join(path_components)
print(modified_path)  # Output: /this/world

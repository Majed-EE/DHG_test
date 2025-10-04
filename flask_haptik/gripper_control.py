'''Gripper Control Module'''

class GripperControl:
    def __init__(self, min_value=0, max_value=100):
        """
        Initialize the GripperControl class with minimum and maximum values.
        :param min_value: Minimum value for the gripper input.
        :param max_value: Maximum value for the gripper input.
        """
        self.min_value = min_value
        self.max_value = max_value

    def process_input(self, input_value):
        """
        Process the input value and return a value suitable for the gripper.
        :param input_value: The input value to process.
        :return: A value scaled and clamped between min_value and max_value.
        """
        # Clamp the input value between min_value and max_value
        clamped_value = max(self.min_value, min(self.max_value, input_value))

        # Scale the value to a range suitable for the gripper (e.g., 0 to 1)
        scaled_value = (clamped_value - self.min_value) / (self.max_value - self.min_value)

        return scaled_value

# Example usage
gripper = GripperControl(min_value=0, max_value=100)
input_value = 75
output_value = gripper.process_input(input_value)
print(f"Processed output for the gripper: {output_value}")


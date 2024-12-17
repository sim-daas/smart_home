import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
        self.gpio_pin = 12
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.LOW)  # Ensure pin is LOW initially

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

        # Check for "thumbs up" and set GPIO accordingly
        if msg.data == "Thumb_Up":
            self.get_logger().info("Thumbs up detected! Setting GPIO 12 HIGH.")
            GPIO.output(self.gpio_pin, GPIO.HIGH)
            time.sleep(1)
        elif msg.data == "Closed_Fist":
            self.get_logger().info("Closed fist detected")
            GPIO.output(self.gpio_pin, GPIO.LOW)
            time.sleep(1)
        else:
            self.get_logger().info("No thumbs up. Setting GPIO 12 LOW.")
            #GPIO.output(self.gpio_pin, GPIO.LOW)

    def destroy_node(self):
        # Cleanup GPIO on shutdown
        GPIO.cleanup()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        minimal_subscriber.get_logger().info("Shutting down...")
    finally:
        # Destroy the node explicitly to ensure GPIO cleanup
        minimal_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

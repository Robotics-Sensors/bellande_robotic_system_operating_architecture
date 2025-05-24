import common_msgs.Messages.*;

public class Example_java {
    public void run() {
        while (true) {
            // TODO: Implement node logic
            System.out.println("Running example_java");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        Example_java node = new Example_java();
        node.run();
    }
}

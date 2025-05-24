import common_msgs.Messages.*;

public class Example_package {
    public void run() {
        while (true) {
            // TODO: Implement node logic
            System.out.println("Running example_package");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        Example_package node = new Example_package();
        node.run();
    }
}

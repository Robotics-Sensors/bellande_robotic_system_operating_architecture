-- brsoa_system_config.lua
-- Global configuration
global_config = {
    max_nodes = 50,
    discovery_method = "broadcast",
    system_name = "example_system",
    log_level = "debug"
}

-- Define nodes to be launched
nodes = {
    {
        name = "example_node_cpp",
        package = "example_package_cpp",
        executable = "example_driver_cpp",
        language = "cpp",
        args = {"--fps=30"},
        env = {SENSOR_TYPE = "lidar"}
    },
    {
        name = "example_node_py",
        package = "example_package_py",
        executable = "example_package_py.py",
        language = "python",
        args = {"--algorithm=detection"},
        env = {PYTHONPATH = "${WORKSPACE}/lib:${WORKSPACE}/include"}
    },
    {
        name = "example_node_java",
        package = "example_ui_package_java",
        executable = "ExampleDisplayAppJava",
        language = "java",
        args = {"--resolution=720p"},
        env = {JAVA_OPTS = "-Xmx1g"}
    },
    {
        name = "example_node_rust",
        package = "example_package_rust",
        executable = "example_package_rust",
        language = "rust",
        args = {"--mode=manual"},
        env = {RUST_BACKTRACE = "1"}
    },
    {
        name = "example_node_bridge_go",
        package = "example_package_go",
        executable = "example_package_go",
        language = "go",
        args = {"--port=9090"},
        env = {GOMAXPROCS = "2"}
    }
}

-- Define communication setup
topics = {
    {
        name = "/example/example",
        type = "Example",
        queue_size = 5,
        publishers = {"example_node"},
        subscribers = {"example1", "example2"}
    }
}

-- Define services
services = {
    {
        name = "/example/example",
        type = "Example",
        server = "example_server",
        clients = {"example_client"}
    }
}

-- Define parameters
parameters = {
    {
        name = "/example/example",
        type = "string",
        value = global_config.system_name
    }
}
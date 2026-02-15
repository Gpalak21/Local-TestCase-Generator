module.exports = {
    apps: [
        {
            name: "backend",
            script: "server.py",
            cwd: "./backend",
            interpreter: "/opt/homebrew/Caskroom/miniconda/base/bin/python",
            watch: true,
            env: {
                PORT: 8000
            }
        },
        {
            name: "frontend",
            script: "/opt/homebrew/Caskroom/miniconda/base/bin/python",
            args: ["-m", "http.server", "8081"],
            cwd: "./frontend",
            interpreter: "none",
            watch: true
        }
    ]
};

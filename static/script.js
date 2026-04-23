function cacheBust(url) {
    return url ? `${url}?${Date.now()}` : "";
}

function measurement(options) {
    return {
        status: "Initializing",
        instruction: "",
        runId: null,
        running: false,
        images: {},
        statusTimer: null,
        imageTimer: null,
        instructionTimer: null,
        start() {
            this.refreshStatus();
            this.refreshImages();
            if (options.instructionUrl) {
                this.refreshInstruction();
            }
            this.statusTimer = setInterval(() => this.refreshStatus(), options.statusMs || 500);
            this.imageTimer = setInterval(() => this.refreshImages(), options.imageMs || 1000);
            if (options.instructionUrl) {
                this.instructionTimer = setInterval(() => this.refreshInstruction(), options.instructionMs || 1000);
            }
        },
        markRunning() {
            this.running = true;
            this.status = "Starting...";
        },
        stop() {
            clearInterval(this.statusTimer);
            clearInterval(this.imageTimer);
            clearInterval(this.instructionTimer);
        },
        isCurrent(data) {
            if (!data.run_id) {
                return true;
            }
            if (this.runId === null) {
                this.runId = data.run_id;
            }
            return this.runId === data.run_id;
        },
        refreshStatus() {
            fetch("/status")
                .then((response) => response.json())
                .then((data) => {
                    if (data.run_id && data.run_id !== this.runId) {
                        this.runId = data.run_id;
                    }
                    this.status = data.status || "";
                    this.running = !/complete|failed|press start/i.test(this.status);
                })
                .catch(() => {
                    this.status = "Status unavailable";
                    this.running = false;
                });
        },
        refreshImages() {
            fetch(options.imageUrl || "/img")
                .then((response) => response.json())
                .then((data) => {
                    if (!this.isCurrent(data)) {
                        return;
                    }
                    Object.keys(data).forEach((key) => {
                        if (key !== "run_id") {
                            this.images[key] = cacheBust(data[key]);
                        }
                    });
                })
                .catch(() => {});
        },
        refreshInstruction() {
            fetch(options.instructionUrl)
                .then((response) => response.json())
                .then((data) => {
                    if (this.isCurrent(data)) {
                        this.instruction = data.instruction || "";
                    }
                })
                .catch(() => {
                    this.instruction = "";
                });
        },
        statusClass() {
            if (/failed|error/i.test(this.status)) {
                return "bg-red-50 text-red-700 ring-red-200";
            }
            if (/complete/i.test(this.status)) {
                return "bg-emerald-50 text-emerald-700 ring-emerald-200";
            }
            return "bg-amber-50 text-amber-800 ring-amber-200";
        }
    };
}

function shutdownServer() {
    fetch("/shutdown", { method: "POST" })
        .then((response) => response.text())
        .then((data) => console.log(data))
        .catch((error) => console.error("Error:", error));
    alert("Service is shutting down");
}

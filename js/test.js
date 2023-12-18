import {app} from "../../scripts/app.js";
import {ComfyWidgets} from "../../scripts/widgets.js";

// Create a read-only string widget with opacity set
function createWidget(app, node, widgetName) {
    const widget = ComfyWidgets["STRING"](node, widgetName, ["STRING", {multiline: true}], app).widget;
    widget.inputEl.readOnly = true;
    widget.inputEl.style.opacity = 0.7;
    return widget;
}

// Displays file list on the node
app.registerExtension({
    name: "sd_prompt_reader.loaderDisplay",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "CR JS Test") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);

                // Create prompt and setting widgets
                const fileList = createWidget(app, this, "fileList");
                return result;
            };

            // Update widgets
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                this.widgets.find(obj => obj.name === "fileList").value = message.text[0];

            };
        }
    },
});
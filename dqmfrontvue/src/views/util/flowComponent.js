import * as joint from "jointjs";

var createFlowComponent = function(id, props, data) {
  var flowComponent = {};
  flowComponent.graph = new joint.dia.Graph(
    {
      /* attributes of the graph */
    },
    { cellNamespace: joint.shapes }
  );
  flowComponent.paper = new joint.dia.Paper({
    cellViewNamespace: joint.shapes,
    el: document.getElementById(id),
    model: flowComponent.graph,
    width: props.width,
    height: props.height,
    gridSize: props.gridSize,
    drawGrid: props.drawGrid,
    background: props.background,
    interactive: !props.readonly
  });
  flowComponent.graph.fromJSON(data);
  return flowComponent;
};

export default createFlowComponent;

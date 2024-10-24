<template>
  <div>
    <div class="flex-container flex-row">
      <div class="flex-item flex-col Shema_item_1">
        <div>
          <h2 class="h2_item">Блоки для схемы</h2>
        </div>
        <div id="flow-component"></div>
      </div>

      <div class="flex-item flex-col Shema_item_2">
       <div id="flow-chart-component"></div>
      </div>
    </div>
  </div>
</template>

<script>
import createFlowComponent from "./util/flowComponent.js";
import * as joint from "jointjs";
import JQuery from "jquery";
import flowComponentsData from "./mock/components-mock";
import flowChartData from "./mock/flow-chart-mock";

let $ = JQuery;

export default {
  name: "FlowGenerator",
  components: {},
  data() {
    return {
      flowComponentsData,
      flowChartData,
      propertyArray: ["Type", "Color", "Context"]
    };
  },

  methods: {
    //Send signals and data to App.vue
    showProperties() {
      eventBus.$emit("displayProperties", this.propertyArray);
    },

 
  },
  mounted() {
    this.flowComponents = createFlowComponent(
      "flow-component",
      {
        width: 100,
        height: 800,
        gridSize: 10,
        drawGrid: { name: "mesh" },
        background: { color: "antiquewhite" },
        readonly: true
      },
      flowComponentsData
    );
    this.flowChartComponent = createFlowComponent(
      "flow-chart-component",
      {
        width: 300,
        height: 800,
        gridSize: 10,
        drawGrid: { name: "mesh" },
        background: { color: "antiquewhite" },
        readonly: false
      },
      flowChartData
    );
    var _this = this;
  
// ------------------------- Стили для стрелок начало
    var verticesTool = new joint.linkTools.Vertices();
    var segmentsTool = new joint.linkTools.Segments();
    var sourceArrowheadTool = new joint.linkTools.SourceArrowhead();
    var targetArrowheadTool = new joint.linkTools.TargetArrowhead();
    var sourceAnchorTool = new joint.linkTools.SourceAnchor();
    var targetAnchorTool = new joint.linkTools.TargetAnchor();
    var boundaryTool = new joint.linkTools.Boundary();
    var removeButton = new joint.linkTools.Remove({
        distance: 20
    });
    var tools = new joint.dia.ToolsView({
      tools: [
          verticesTool,
          segmentsTool,
          // sourceArrowheadTool,
          targetArrowheadTool,
          // sourceAnchorTool,
          // targetAnchorTool,
          boundaryTool,
          removeButton
      ]
    });
// ------------------------- Стили для стрелок конец

// ------------------------- Стили для Блоков начало
    var boundaryTool = new joint.elementTools.Boundary();
    var connectTool = new joint.elementTools.Connect(    {

        x: '100%',
        y: '50%',
        offset: {
            x: 0,
            y: 0
        },

        rotate: true,
    });
    var removeButton = new joint.elementTools.Remove(
    {
        x: '0%',
        y: '50%',
        offset: {
            x: 0,
            y: 0
        },
        rotate: true,

    });
  
    
    var toolsView = new joint.dia.ToolsView({
        tools: [boundaryTool, removeButton, connectTool]
    });
// ------------------------- Стили для Блоков конец

    // Перетаскивание ячеек между двумя страницами
    this.flowComponents.paper.on("cell:pointerdown", (cellView, e, x, y) => {
      $("body").append(
        '<div id="flyPaper" style="position:fixed;z-index:100;opacity:.7;pointer-event:none;"></div>'
      );
    var flyGraph = new joint.dia.Graph(),
        flyShape = cellView.model.clone(),
        flyPaper = new joint.dia.Paper({
            el: $("#flyPaper"),
            model: flyGraph,
            interactive: false,
            width: flyShape.attributes.size.width,
            height: flyShape.attributes.size.height
        }),
        pos = cellView.model.position(),
        offset = {
          x: x - pos.x,
          y: y - pos.y
        };

      flyShape.position(0, 0);
      flyGraph.addCell(flyShape);

      $("#flyPaper").offset({
        left: e.pageX - offset.x,
        top: e.pageY - offset.y
      });

      $("body").on("mousemove.fly", function(e) {
        $("#flyPaper").offset({
          left: e.pageX - offset.x,
          top: e.pageY - offset.y
        });
      });
      $("body").on("mouseup.fly", function(e) {
        var x = e.pageX,
          y = e.pageY,
          target = _this.flowChartComponent.paper.$el.offset();

        // Dropped over paper ?
        if (
          x > target.left &&
          x < target.left + _this.flowChartComponent.paper.$el.width() &&
          y > target.top &&
          y < target.top + _this.flowChartComponent.paper.$el.height()
        ) {
          var s = flyShape.clone();
          s.position(x - target.left - offset.x, y - target.top - offset.y);
          _this.flowChartComponent.graph.addCell(s);
        }
        $("body")
          .off("mousemove.fly")
          .off("mouseup.fly");
        flyShape.remove();
        $("#flyPaper").remove();
      });
    });

    // Создание связей между двумя ячейками

    this.flowChartComponent.paper.on({
      "element:pointerdown": function(elementView, evt) {
        evt.data = elementView.model.position();
     
        
      },
      "element:pointerup": function(elementView, evt, x, y) {

        var coordinates = new joint.g.Point(x, y);
        var elementAbove = elementView.model;
        var elementBelow = this.model
          .findModelsFromPoint(coordinates)
          .find(function(el) {
            return el.id !== elementAbove.id;
          });

        // Если два элемента уже подключены, не
        // подключайте их снова (хотя это зависит от конкретного приложения).
        if (
          elementBelow &&
          _this.flowChartComponent.graph
            .getNeighbors(elementBelow)
            .indexOf(elementAbove) === -1
        ) {
          // Переместите элемент в нужное положение перед перетаскиванием
          elementAbove.position(evt.data.x, evt.data.y);
          
          // Create a connection between elements.
          var link = new joint.shapes.standard.Link();
          link.source(elementAbove);
          link.target(elementBelow);
          link.addTo(_this.flowChartComponent.graph);
          
        }
      
      },
      "link:mouseenter": function(elementView) {
        elementView.addTools(tools);
      },
      "link:mouseleave": function(elementView) {
        elementView.removeTools();
      },

      "element:mouseenter": function(elementView) {
        elementView.addTools(toolsView);
      },
      "element:mouseleave": function(elementView) {
        elementView.removeTools();
      }
      //Show element properties when clicked
      // "element:pointerclick": function(elementView, evt) {
      
      //   this.showProperties();
      // }
    });





  }
  
};
</script>

<style lang="scss">
@import "@/utils/colors.scss";
div #flow-component, div #flow-chart-component  {
    width: 100% !important;
    height: 99% !important;
}

div #flow-chart-component  {
    background: rgb(247, 247, 247) !important;
}

.Shema_item_1 {
    width: 20%;
}

.Shema_item_2 {
width: 80%;

}
.h2_item {
    text-align: center;
    font-size: 1.5rem!important;
}



</style>


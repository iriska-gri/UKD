export default {
    cells: [
      {
        type: "standard.Rectangle",
        position: { x: 20, y: 30 },
        size: { width: 200, height: 40 },
        angle: 0,
        id: "d5f0a1ed-422a-447d-8196-ec60918e197c",
        z: 1,
        attrs: {
            body: {
                fill: "green"
            },
            label: {
                fill: "white",
                text: "Стол"
            } }
      },
    //   {
    //     type: "standard.BorderedImage",
    //     position: { x: 20, y: 110 },
    //     size: { width: 50, height: 50 },
    //     angle: 0,
    //     id: "c3ca25dd-805d-4a01-9f85-583b0c0f8e3a",
    //     z: 1,
    //     attrs: {
    //       border: { rx: 5 },
    //       image: { xlinkHref: "email-img.png" },
    //       label: { text: "Email" },
    //       root: { title: "joint.shapes.standard.BoarderedImage" }
    //     }
    //   },
   
      {
        type: "standard.Polygon",
        position: { x: 20, y: 90 },
        size: { width: 100, height: 100 },
        angle: 0,
        id: "355395e1-ac4a-4b4e-b85f-49b22c327386",
        z: 2,
        attrs: {
          body: { refPoints: "0,10 10,0 20,10 10,20" },
          label: { text: "Идешь?" },
          root: { title: "joint.shapes.standard.Polygon" }
        }
      },

      {
        type: "standard.Rectangle",
        position: { x: 20, y: 200 },
        size: { width: 50, height: 50 },
        angle: 0,
        id: "d5f0a1ed-422a-447d-8196-ec60918e197d",
        z: 1,
        attrs: {
            body: {
                fill: "blue"
            },
            label: {
                fill: "white",
                text: "Человек"
            } }
      },


      
    ]
  };
  
const SERVER_URL = "http://159.203.158.171";

async function fetchTreeData(traceID) {
  try {
    const response = await fetch(`${SERVER_URL}/graph?traceId=${traceID}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching tree data:", error);
    return null;
  }
}

function clearSvg() {
  d3.selectAll("svg").remove();
}

function drawTree(traceID, treeData, containerSelector) {
  // Set up the tree layout
  const treeLayout = d3.tree().size([500, 300]);

  const svg = d3
    .select(containerSelector)
    .append("svg")
    .attr("width", 600)
    .attr("height", 550)
    .append("g")
    .attr("transform", "translate(150,10)");

  // Add a title for the graph
  svg
    .append("text")
    .attr("class", "graph-title")
    .attr("x", 150) // Adjust the x position to center the title
    .attr("y", 40) // Adjust the y position based on your preference
    .text(`Network Graph - ${traceID}`);

  // Create a hierarchy from the data
  const root = d3.hierarchy(treeData);

  // Assign positions to each node in the hierarchy
  treeLayout(root);

  // Draw links between nodes
  svg
    .selectAll("path.link")
    .data(root.links())
    .enter()
    .append("path")
    .attr("class", "link")
    .attr(
      "d",
      d3
        .linkHorizontal()
        .x((d) => d.y)
        .y((d) => d.x)
    );

  // Draw nodes
  const node = svg
    .selectAll("g.node")
    .data(root.descendants())
    .enter()
    .append("g")
    .attr("class", "node")
    .attr("transform", (d) => `translate(${d.y},${d.x})`);

  // Add circles with radius based on the data
  node
    .append("circle")
    .attr("r", (d) => d.data.processingTime + 7 || 7)
    .style("fill", (d) => (d.data.isComplete === true ? "green" : "gray"));
  // .attr("r", 7);

  // Add text labels to nodes
  node
    .append("text")
    .attr("dy", ".31em")
    .attr("x", (d) => (d.children ? -15 : 15))
    .style("text-anchor", (d) => (d.children ? "end" : "start"))
    .text(
      (d) =>
        `${d.data.name} (${
          d.data.processingTime === null ? "NA" : d.data.processingTime + "s"
        }) `
    );
}

document.addEventListener("DOMContentLoaded", function () {
  fetch(`${SERVER_URL}/trace`)
    .then((response) => response.json())
    .then((jsonData) => {
      // Create a table element
      var table = document.createElement("table");

      // Create table header
      var thead = table.createTHead();
      var headerRow = thead.insertRow();
      Object.keys(jsonData[0]).forEach(function (key) {
        var th = document.createElement("th");
        th.textContent = key;
        headerRow.appendChild(th);
      });

      // Create table body
      var tbody = table.createTBody();
      jsonData.forEach(function (rowData) {
        var row = tbody.insertRow();
        Object.values(rowData).forEach(function (value) {
          var cell = row.insertCell();
          cell.textContent = value;
        });

        // Add click event listener to each row
        row.addEventListener("click", function () {
          // Display the 'trace_id' in an alert box
          clearSvg();
          drawTreeFromServer("#graph", rowData.trace_id);
        });
      });

      // Append the table to the "table-section" div
      document.getElementById("table-section").appendChild(table);
    })
    .catch((error) => console.error("Error fetching data:", error));
});

function sleep(delay) {
  var start = new Date().getTime();
  while (new Date().getTime() < start + delay);
}

async function drawTreeFromServer(containerSelector, traceID) {
  // Fetch tree data
  const treeData = await fetchTreeData(traceID);

  if (!treeData) {
    console.error("Tree data is null or undefined.");
    return;
  }
  drawTree(traceID, treeData, containerSelector);

  // todo: fix this
  while (treeData.isComplete === false) {
    sleep(2);
    clearSvg();
    drawTree(traceID, treeData, containerSelector);
  }
}

// Call the modified function with the container selector
// drawTreeFromServer('#graph');

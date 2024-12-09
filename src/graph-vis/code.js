document.addEventListener("DOMContentLoaded", function() {
    d3.json("data.json").then(function(data) {
        const width = 800;
        const height = 600;

        const svg = d3.select("#canvas")
            .attr("width", width)
            .attr("height", height)
            .call(d3.zoom().on("zoom", function (event) {
                svg.attr("transform", event.transform);
            }))
            .append("g");

        const root = d3.hierarchy(data);

        const treeLayout = d3.tree().nodeSize([15, 60]);
        treeLayout(root);

        // Links
        svg.selectAll('path.link')
            .data(root.links())
            .enter()
            .append('path')
            .attr('class', 'link')
            .attr('d', d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x)
            );

        // Additional links for other_calls
        root.descendants().forEach(d => {
            if (d.data.other_calls) {
                d.data.other_calls.forEach(call => {
                    const target = root.descendants().find(node => node.data.full_name === call);
                    if (target) {
                        svg.append('path')
                            .attr('class', 'other-link')
                            .attr('d', d3.linkHorizontal()({
                                source: [d.y, d.x],
                                target: [target.y, target.x]
                            }));
                    }
                });
            }
        });

        // Nodes
        const node = svg.selectAll('g.node')
            .data(root.descendants())
            .enter()
            .append('g')
            .attr('class', 'node')
            .attr('transform', d => `translate(${d.y},${d.x})`);

        node.append('circle')
            .attr('r', 5)
            .attr('status', d => d.data.metadata.error ? 'error' : 'ok');

        node.append('text')
            .attr('dy', 3)
            .attr('x', d => d.children ? -8 : 8)
            .style('text-anchor', d => d.children ? 'end' : 'start')
            .text(d => d.data.name);

        // Add link to node.data.url if defined
        node.filter(d => d.data.metadata.url)
            .append('a')
            .attr('xlink:href', d => d.data.metadata.url)
            .attr('target', '_blank')
            .append('text')
            .attr('dy', 3)
            .attr('x', d => d.children ? -8 : 8)
            .style('text-anchor', d => d.children ? 'end' : 'start')
            .text(d => d.data.name);
    });
});

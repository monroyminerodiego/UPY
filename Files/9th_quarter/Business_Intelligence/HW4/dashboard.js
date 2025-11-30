// Dashboard Controller
class DashboardController {
    constructor() {
        this.currentView = 'eda';
        this.data = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Navigation tabs
        document.getElementById('tab-eda').addEventListener('click', () => this.switchView('eda'));
        document.getElementById('tab-modeling').addEventListener('click', () => this.switchView('modeling'));
        document.getElementById('tab-analysis').addEventListener('click', () => this.switchView('analysis'));
        
        // Store selector
        const storeSelector = document.getElementById('store-selector');
        if (storeSelector) {
            storeSelector.addEventListener('change', (e) => this.updateStoreMix(e.target.value));
        }
    }

    async switchView(viewName) {
        // Update navigation
        document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
        document.getElementById(`tab-${viewName}`).classList.add('active');
        
        // Hide all views
        document.querySelectorAll('.view-content').forEach(view => view.classList.add('hidden'));
        
        // Show selected view
        document.getElementById(`view-${viewName}`).classList.remove('hidden');
        document.getElementById(`view-${viewName}`).classList.add('fade-in');
        
        this.currentView = viewName;
        
        // Load view-specific data
        await this.loadViewData(viewName);
    }

    async loadInitialData() {
        try {
            const edaResponse = await fetch('/business-intelligence/bigmart-analisys/eda-summary');
            if (edaResponse.ok) {
                this.data.eda = await edaResponse.json();
                this.updateEDASummary();
            }
            
            const distResponse = await fetch('/business-intelligence/bigmart-analisys/distributions');
            if (distResponse.ok) {
                this.data.distributions = await distResponse.json();
                this.createHistograms();
            }
            
            const outliersResponse = await fetch('/business-intelligence/bigmart-analisys/outliers');
            if (outliersResponse.ok) {
                this.data.outliers = await outliersResponse.json();
                this.updateOutliersAnalysis();
            }
            
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadViewData(viewName) {
        try {
            switch(viewName) {
                case 'modeling':
                    await this.loadModelingData();
                    break;
                case 'analysis':
                    await this.loadAnalysisData();
                    break;
            }
        } catch (error) {
            console.error(`Error loading ${viewName} data:`, error);
        }
    }

    async loadModelingData() {
        try {
            const metricsResponse = await fetch('/business-intelligence/bigmart-analisys/clustering-metrics');
            if (metricsResponse.ok) {
                this.data.clusteringMetrics = await metricsResponse.json();
                this.createClusteringCharts();
            }
            
            const pcaResponse = await fetch('/business-intelligence/bigmart-analisys/pca-visualization');
            if (pcaResponse.ok) {
                this.data.pcaData = await pcaResponse.json();
                this.createPCAVisualization();
            }
        } catch (error) {
            console.error('Error loading modeling data:', error);
        }
    }

    async loadAnalysisData() {
        try {
            const profilesResponse = await fetch('/business-intelligence/bigmart-analisys/cluster-profiles');
            if (profilesResponse.ok) {
                this.data.clusterProfiles = await profilesResponse.json();
                this.updateClusterProfiles();
            }
            
            const storeMixResponse = await fetch('/business-intelligence/bigmart-analisys/store-mix-analysis');
            if (storeMixResponse.ok) {
                this.data.storeMix = await storeMixResponse.json();
                this.populateStoreSelector();
                this.createStoreMixChart();
            }
            
            const hierarchyResponse = await fetch('/business-intelligence/bigmart-analisys/store-hierarchy');
            if (hierarchyResponse.ok) {
                this.data.storeHierarchy = await hierarchyResponse.json();
                this.createHierarchyVisualization();
            }
        } catch (error) {
            console.error('Error loading analysis data:', error);
        }
    }

    updateEDASummary() {
        if (!this.data.eda) return;
        
        document.getElementById('total-records').textContent = this.data.eda.total_records.toLocaleString();
        document.getElementById('unique-products').textContent = this.data.eda.unique_products.toLocaleString();
        document.getElementById('unique-stores').textContent = this.data.eda.unique_stores.toLocaleString();
        document.getElementById('total-features').textContent = this.data.eda.total_features;
        
        const missingContainer = document.getElementById('missing-values');
        missingContainer.innerHTML = `
            <div class="space-y-3">
                <div class="flex justify-between items-center p-3 bg-yellow-50 rounded-lg">
                    <span class="font-medium">Item_Weight</span>
                    <div class="text-right">
                        <span class="text-sm text-gray-600">${this.data.eda.missing_values.Item_Weight.count} registros</span>
                        <div class="text-xs text-gray-500">${this.data.eda.missing_values.Item_Weight.percentage.toFixed(1)}%</div>
                    </div>
                </div>
                <div class="flex justify-between items-center p-3 bg-orange-50 rounded-lg">
                    <span class="font-medium">Outlet_Size</span>
                    <div class="text-right">
                        <span class="text-sm text-gray-600">${this.data.eda.missing_values.Outlet_Size.count} registros</span>
                        <div class="text-xs text-gray-500">${this.data.eda.missing_values.Outlet_Size.percentage.toFixed(1)}%</div>
                    </div>
                </div>
            </div>
        `;
        
        const categoryContainer = document.getElementById('category-distributions');
        const fatContent = this.data.eda.fat_content_dist;
        const outletType = this.data.eda.outlet_type_dist;
        
        categoryContainer.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-medium text-gray-700 mb-2">Contenido Graso</h4>
                    ${Object.entries(fatContent).map(([key, value]) => `
                        <div class="flex justify-between text-sm">
                            <span>${key}</span>
                            <span class="font-medium">${value}</span>
                        </div>
                    `).join('')}
                </div>
                <div>
                    <h4 class="font-medium text-gray-700 mb-2">Tipo de Tienda</h4>
                    ${Object.entries(outletType).map(([key, value]) => `
                        <div class="flex justify-between text-sm">
                            <span>${key}</span>
                            <span class="font-medium">${value}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    createHistograms() {
        if (!this.data.distributions) return;
        
        this.createHistogram('sales-histogram', this.data.distributions.sales, 'Ventas', '#10b981');
        this.createHistogram('mrp-histogram', this.data.distributions.mrp, 'Precio MRP', '#3b82f6');
    }

    createHistogram(containerId, data, title, color) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = '';
        
        const margin = {top: 20, right: 20, bottom: 40, left: 40};
        const width = container.offsetWidth - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        data = data.filter(d => d !== null && d !== undefined && !isNaN(d));
        
        const xScale = d3.scaleLinear()
            .domain(d3.extent(data))
            .range([0, width]);
        
        const histogram = d3.histogram()
            .domain(xScale.domain())
            .thresholds(20);
        
        const bins = histogram(data);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(bins, d => d.length)])
            .range([height, 0]);
        
        svg.selectAll('rect')
            .data(bins)
            .enter()
            .append('rect')
            .attr('x', d => xScale(d.x0))
            .attr('y', d => yScale(d.length))
            .attr('width', d => xScale(d.x1) - xScale(d.x0) - 1)
            .attr('height', d => height - yScale(d.length))
            .attr('fill', color)
            .attr('opacity', 0.7);
        
        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis);
        
        svg.append('g')
            .call(yAxis);
        
        svg.append('text')
            .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 5})`)
            .style('text-anchor', 'middle')
            .text(title);
    }

    updateOutliersAnalysis() {
        if (!this.data.outliers) return;
        
        const container = document.getElementById('outliers-analysis');
        container.innerHTML = '';
        
        Object.entries(this.data.outliers).forEach(([column, data]) => {
            const card = document.createElement('div');
            card.className = 'p-4 bg-red-50 rounded-lg';
            card.innerHTML = `
                <h4 class="font-bold text-red-800 mb-2">${column.replace(/_/g, ' ')}</h4>
                <div class="space-y-2">
                    <div class="text-sm">
                        <span class="text-gray-600">Outliers:</span>
                        <span class="font-bold text-red-900">${data.count} (${data.percentage.toFixed(1)}%)</span>
                    </div>
                    <div class="text-xs text-gray-500">
                        Rango: ${data.lower_bound.toFixed(2)} - ${data.upper_bound.toFixed(2)}
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    createClusteringCharts() {
        if (!this.data.clusteringMetrics) return;
        
        this.createSilhouetteChart();
        this.createInertiaChart();
    }

    createSilhouetteChart() {
        const container = document.getElementById('silhouette-chart');
        if (!container) return;
        
        const margin = {top: 20, right: 20, bottom: 40, left: 40};
        const width = container.offsetWidth - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;
        
        container.innerHTML = '';
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        const data = this.data.clusteringMetrics.k_range.map((k, i) => ({
            k: k,
            score: this.data.clusteringMetrics.silhouette_scores[i]
        }));
        
        const xScale = d3.scaleLinear()
            .domain(d3.extent(data, d => d.k))
            .range([0, width]);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.score)])
            .range([height, 0]);
        
        const line = d3.line()
            .x(d => xScale(d.k))
            .y(d => yScale(d.score))
            .curve(d3.curveMonotoneX);
        
        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#3b82f6')
            .attr('stroke-width', 2)
            .attr('d', line);
        
        svg.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d.k))
            .attr('cy', d => yScale(d.score))
            .attr('r', 4)
            .attr('fill', '#3b82f6');
        
        const optimal = data.find(d => d.k === this.data.clusteringMetrics.optimal_k);
        if (optimal) {
            svg.append('circle')
                .attr('cx', xScale(optimal.k))
                .attr('cy', yScale(optimal.score))
                .attr('r', 8)
                .attr('fill', '#ef4444')
                .attr('stroke', '#fff')
                .attr('stroke-width', 2);
        }
        
        const xAxis = d3.axisBottom(xScale).ticks(10);
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis);
        
        svg.append('g')
            .call(yAxis);
        
        svg.append('text')
            .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 5})`)
            .style('text-anchor', 'middle')
            .text('Número de Clusters (K)');
        
        svg.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 0 - margin.left)
            .attr('x', 0 - (height / 2))
            .attr('dy', '1em')
            .style('text-anchor', 'middle')
            .text('Puntaje Silhouette');
    }

    createInertiaChart() {
        const container = document.getElementById('inertia-chart');
        if (!container) return;
        
        const margin = {top: 20, right: 20, bottom: 40, left: 40};
        const width = container.offsetWidth - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;
        
        container.innerHTML = '';
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        const data = this.data.clusteringMetrics.k_range.map((k, i) => ({
            k: k,
            inertia: this.data.clusteringMetrics.inertia_values[i]
        }));
        
        const xScale = d3.scaleLinear()
            .domain(d3.extent(data, d => d.k))
            .range([0, width]);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.inertia)])
            .range([height, 0]);
        
        const line = d3.line()
            .x(d => xScale(d.k))
            .y(d => yScale(d.inertia))
            .curve(d3.curveMonotoneX);
        
        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', '#8b5cf6')
            .attr('stroke-width', 2)
            .attr('d', line);
        
        svg.selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d.k))
            .attr('cy', d => yScale(d.inertia))
            .attr('r', 4)
            .attr('fill', '#8b5cf6');
        
        const xAxis = d3.axisBottom(xScale).ticks(10);
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis);
        
        svg.append('g')
            .call(yAxis);
        
        svg.append('text')
            .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 5})`)
            .style('text-anchor', 'middle')
            .text('Número de Clusters (K)');
        
        svg.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 0 - margin.left)
            .attr('x', 0 - (height / 2))
            .attr('dy', '1em')
            .style('text-anchor', 'middle')
            .text('Inercia');
    }

    createPCAVisualization() {
        const container = document.getElementById('pca-visualization');
        if (!container || !this.data.pcaData) return;
        
        const margin = {top: 20, right: 20, bottom: 40, left: 40};
        const width = container.offsetWidth - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;
        
        container.innerHTML = '';
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        const xScale = d3.scaleLinear()
            .domain(d3.extent(this.data.pcaData, d => d.pc1))
            .range([0, width]);
        
        const yScale = d3.scaleLinear()
            .domain(d3.extent(this.data.pcaData, d => d.pc2))
            .range([height, 0]);
        
        const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
        
        svg.selectAll('circle')
            .data(this.data.pcaData)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d.pc1))
            .attr('cy', d => yScale(d.pc2))
            .attr('r', 3)
            .attr('fill', d => colorScale(d.cluster))
            .attr('opacity', 0.7);
        
        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);
        
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis);
        
        svg.append('g')
            .call(yAxis);
        
        svg.append('text')
            .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 5})`)
            .style('text-anchor', 'middle')
            .text('Primera Componente Principal');
        
        svg.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 0 - margin.left)
            .attr('x', 0 - (height / 2))
            .attr('dy', '1em')
            .style('text-anchor', 'middle')
            .text('Segunda Componente Principal');
        
        const legend = svg.append('g')
            .attr('transform', `translate(${width - 100}, 20)`);
        
        const clusters = [...new Set(this.data.pcaData.map(d => d.cluster))];
        clusters.forEach((cluster, i) => {
            const legendRow = legend.append('g')
                .attr('transform', `translate(0, ${i * 20})`);
            
            legendRow.append('rect')
                .attr('width', 10)
                .attr('height', 10)
                .attr('fill', colorScale(cluster));
            
            legendRow.append('text')
                .attr('x', 15)
                .attr('y', 10)
                .text(`Cluster ${cluster}`)
                .style('font-size', '12px');
        });
    }

    updateClusterProfiles() {
        if (!this.data.clusterProfiles) return;
        
        const container = document.getElementById('cluster-profiles');
        container.innerHTML = '';
        
        const colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b'];
        
        this.data.clusterProfiles.forEach((profile, index) => {
            const card = document.createElement('div');
            card.className = 'p-6 rounded-xl';
            card.style.background = `linear-gradient(135deg, ${colors[index]}20, ${colors[index]}10)`;
            card.innerHTML = `
                <div class="text-center">
                    <div class="w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center text-white text-2xl font-bold" style="background-color: ${colors[index]}">
                        ${profile.cluster_id}
                    </div>
                    <h4 class="font-bold text-gray-800 mb-2">${profile.cluster_label}</h4>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span>Productos:</span>
                            <span class="font-medium">${profile.count}</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Ventas Prom:</span>
                            <span class="font-medium">${profile.avg_sales.toFixed(0)}</span>
                        </div>
                        <div class="flex justify-between">
                            <span>MRP Prom:</span>
                            <span class="font-medium">${profile.avg_mrp.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Tiendas:</span>
                            <span class="font-medium">${profile.avg_store_count.toFixed(1)}</span>
                        </div>
                    </div>
                    <div class="mt-3 text-xs text-gray-600">
                        <strong>Categoría:</strong> ${profile.dominant_category}
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    populateStoreSelector() {
        if (!this.data.storeMix) return;
        
        const selector = document.getElementById('store-selector');
        selector.innerHTML = '<option value="">Seleccione una tienda...</option>';
        
        this.data.storeMix.forEach(store => {
            const option = document.createElement('option');
            option.value = store.store_id;
            option.textContent = `${store.store_id} (${store.store_type})`;
            selector.appendChild(option);
        });
    }

    createStoreMixChart() {
        // Default chart with all stores
        this.updateStoreMix('');
    }

    updateStoreMix(storeId) {
        const container = document.getElementById('store-mix-chart');
        if (!container || !this.data.storeMix) return;
        
        const margin = {top: 20, right: 20, bottom: 40, left: 40};
        const width = container.offsetWidth - margin.left - margin.right - 150;
        const height = 400 - margin.top - margin.bottom;
        
        container.innerHTML = '';
        
        let data;
        if (storeId) {
            const storeData = this.data.storeMix.find(store => store.store_id === storeId);
            if (!storeData) return;
            data = storeData.mix;
        } else {
            // Aggregate all stores
            const aggregated = {};
            this.data.storeMix.forEach(store => {
                store.mix.forEach(mix => {
                    if (!aggregated[mix.cluster_id]) {
                        aggregated[mix.cluster_id] = {
                            cluster_id: mix.cluster_id,
                            cluster_label: mix.cluster_label,
                            sales: 0,
                            percentage: 0
                        };
                    }
                    aggregated[mix.cluster_id].sales += mix.sales;
                });
            });
            
            // CORRECCIÓN AQUÍ: Usar reduce correctamente
            const totalSales = Object.values(aggregated).reduce((sum, d) => sum + d.sales, 0);
            Object.values(aggregated).forEach(item => {
                item.percentage = (item.sales / totalSales) * 100;
            });
            
            data = Object.values(aggregated);
        }
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width + margin.left + margin.right + 150)
            .attr('height', height + margin.top + margin.bottom);
        
        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        const radius = Math.min(width, height) / 2 - 20;
        
        const pie = d3.pie()
            .value(d => d.percentage);
        
        const arc = d3.arc()
            .innerRadius(radius * 0.4)
            .outerRadius(radius);
        
        const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
        
        const pieG = g.append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);
        
        const arcs = pieG.selectAll('path')
            .data(pie(data))
            .enter()
            .append('g');
        
        arcs.append('path')
            .attr('d', arc)
            .attr('fill', d => colorScale(d.data.cluster_id))
            .attr('stroke', '#fff')
            .attr('stroke-width', 2);
        
        arcs.append('text')
            .attr('transform', d => `translate(${arc.centroid(d)})`)
            .attr('text-anchor', 'middle')
            .text(d => `${d.data.percentage.toFixed(1)}%`)
            .style('font-size', '12px')
            .style('fill', '#fff')
            .style('font-weight', 'bold');
        
        const legend = g.append('g')
            .attr('transform', `translate(${width + 20}, 20)`);
        
        data.forEach((d, i) => {
            const legendRow = legend.append('g')
                .attr('transform', `translate(0, ${i * 20})`);
            
            legendRow.append('rect')
                .attr('width', 10)
                .attr('height', 10)
                .attr('fill', colorScale(d.cluster_id));
            
            legendRow.append('text')
                .attr('x', 15)
                .attr('y', 10)
                .text(`Cluster ${d.cluster_id}: ${d.cluster_label}`)
                .style('font-size', '12px');
        });
        
        g.append('text')
            .attr('x', width / 2)
            .attr('y', -10)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .style('font-weight', 'bold')
            .text(storeId ? `Mezcla de Clusters - Tienda ${storeId}` : 'Mezcla de Clusters - Todas las Tiendas');
    }

    createHierarchyVisualization() {
        const container = document.getElementById('store-hierarchy');
        if (!container || !this.data.storeHierarchy) return;
        
        container.innerHTML = '';
        
        const margin = {top: 20, right: 20, bottom: 20, left: 20};
        const width = container.offsetWidth - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);
        
        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        // Build hierarchy from flat data: Type -> Location -> Store
        const rootData = {
            name: 'BigMart',
            children: []
        };
        
        const byType = {};
        this.data.storeHierarchy.forEach(store => {
            if (!byType[store.type]) {
                byType[store.type] = {};
            }
            if (!byType[store.type][store.location]) {
                byType[store.type][store.location] = [];
            }
            byType[store.type][store.location].push({
                ...store,
                name: store.id,
                value: store.total_sales
            });
        });
        
        Object.entries(byType).forEach(([type, locations]) => {
            const typeNode = {
                name: type,
                children: []
            };
            
            Object.entries(locations).forEach(([location, stores]) => {
                typeNode.children.push({
                    name: location,
                    children: stores
                });
            });
            
            rootData.children.push(typeNode);
        });
        
        const root = d3.hierarchy(rootData)
            .sum(d => d.value || 0)
            .sort((a, b) => b.value - a.value);
        
        const treemap = d3.treemap()
            .size([width, height])
            .padding(2)
            .round(true);
        
        treemap(root);
        
        const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
        
        const leaf = g.selectAll('g')
            .data(root.leaves())
            .enter().append('g')
            .attr('transform', d => `translate(${d.x0},${d.y0})`);
        
        leaf.append('rect')
            .attr('width', d => d.x1 - d.x0)
            .attr('height', d => d.y1 - d.y0)
            .attr('fill', d => {
                if (d.depth === 3) {
                    return d3.color(colorScale(d.parent.parent.data.name)).brighter(0.8);
                }
                return '#ecf0f1';
            })
            .attr('stroke', '#fff')
            .attr('stroke-width', 1)
            .style('cursor', 'pointer')
            .on('mouseover', function(event, d) {
                d3.select(this).attr('opacity', 0.8);
                
                const tooltip = d3.select('body').append('div')
                    .attr('class', 'tooltip-hierarchy')
                    .style('opacity', 0)
                    .style('position', 'absolute')
                    .style('background', 'rgba(0, 0, 0, 0.8)')
                    .style('color', 'white')
                    .style('padding', '8px 12px')
                    .style('border-radius', '5px')
                    .style('font-size', '12px')
                    .style('pointer-events', 'none')
                    .style('z-index', '1000');
                
                let content = `<strong>${d.data.name}</strong><br/>`;
                if (d.depth === 3) {
                    content += `Tipo: ${d.data.type}<br/>
                               Ubicación: ${d.data.location}<br/>
                               Ventas: $${d.data.total_sales?.toLocaleString()}<br/>
                               Tamaño: ${d.data.size}<br/>
                               Año: ${d.data.year_established}`;
                }
                
                tooltip.html(content)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px')
                    .transition()
                    .duration(200)
                    .style('opacity', 0.9);
                
                d3.select(this).on('mouseout', function() {
                    d3.select(this).attr('opacity', 1);
                    tooltip.remove();
                });
            });
        
        leaf.append('text')
            .attr('x', 4)
            .attr('y', 15)
            .style('font-size', d => {
                const width = d.x1 - d.x0;
                const height = d.y1 - d.y0;
                if (width < 60 || height < 40) return '8px';
                if (width < 100 || height < 50) return '10px';
                return '12px';
            })
            .style('fill', '#2c3e50')
            .text(d => {
                const width = d.x1 - d.x0;
                if (width < 40) return '';
                
                const label = d.data.name;
                if (d.depth === 3 && width > 80) {
                    return label.length > 10 ? label.substring(0, 8) + '...' : label;
                }
                return '';
            });
        
        g.append('text')
            .attr('x', width / 2)
            .attr('y', -5)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .style('font-weight', 'bold')
            .text('Jerarquía de Tiendas por Tipo y Ubicación');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new DashboardController();
});
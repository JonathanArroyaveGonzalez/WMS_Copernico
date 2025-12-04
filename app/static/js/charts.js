/**
 * Dashboard Charts - ECharts Implementation
 * Sistema de gráficas interactivas para el dashboard
 */

// Colores del tema
const chartColors = {
    purple: '#8b5cf6',
    pink: '#ec4899',
    blue: '#3b82f6',
    cyan: '#06b6d4',
    green: '#10b981',
    yellow: '#f59e0b',
    red: '#ef4444',
    orange: '#f97316',
    indigo: '#6366f1',
    teal: '#14b8a6'
};

// Paleta de colores para gráficas
const colorPalette = [
    chartColors.purple,
    chartColors.pink,
    chartColors.cyan,
    chartColors.green,
    chartColors.yellow,
    chartColors.blue,
    chartColors.orange,
    chartColors.indigo,
    chartColors.teal,
    chartColors.red
];

// Configuración base del tema oscuro
const darkTheme = {
    backgroundColor: 'transparent',
    textStyle: {
        color: '#9ca3af'
    },
    title: {
        textStyle: {
            color: '#e0e0e0'
        }
    },
    legend: {
        textStyle: {
            color: '#9ca3af'
        }
    },
    tooltip: {
        backgroundColor: 'rgba(30, 30, 46, 0.95)',
        borderColor: 'rgba(139, 92, 246, 0.3)',
        textStyle: {
            color: '#e0e0e0'
        }
    }
};

// Instancias de gráficas
let charts = {};

/**
 * Inicializa todas las gráficas cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', function() {
    if (typeof window.chartData !== 'undefined') {
        initializeCharts(window.chartData);
    }
    
    // Redimensionar gráficas al cambiar tamaño de ventana
    window.addEventListener('resize', function() {
        Object.values(charts).forEach(chart => {
            if (chart) chart.resize();
        });
    });
});

/**
 * Inicializa todas las gráficas con los datos proporcionados
 */
function initializeCharts(data) {
    initVentasMesChart(data.ventas_por_mes || []);
    initProductosCategoriaChart(data.productos_por_categoria || []);
    initTopProductosChart(data.top_productos || []);
    initStockCategoriaChart(data.stock_por_categoria || []);
}

/**
 * Gráfica de Ventas por Mes (Línea/Área)
 */
function initVentasMesChart(data) {
    const container = document.getElementById('ventas-mes-chart');
    if (!container) return;
    
    if (data.length === 0) {
        showNoDataMessage(container, 'No hay datos de ventas disponibles');
        return;
    }
    
    const chart = echarts.init(container);
    charts['ventas-mes'] = chart;
    
    const option = {
        ...darkTheme,
        tooltip: {
            ...darkTheme.tooltip,
            trigger: 'axis',
            formatter: function(params) {
                const d = params[0];
                return `<strong>${d.name}</strong><br/>
                        <span style="color:${chartColors.purple}">●</span> Total: $${d.value.toLocaleString('es-MX', {minimumFractionDigits: 2})}<br/>
                        <span style="color:${chartColors.cyan}">●</span> Cantidad: ${data[d.dataIndex].cantidad} ventas`;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            top: '10%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.map(d => d.mes),
            axisLine: { lineStyle: { color: '#4b5563' } },
            axisLabel: { color: '#9ca3af' }
        },
        yAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: '#4b5563' } },
            axisLabel: { 
                color: '#9ca3af',
                formatter: value => '$' + (value / 1000).toFixed(0) + 'k'
            },
            splitLine: { lineStyle: { color: 'rgba(75, 85, 99, 0.3)' } }
        },
        series: [{
            name: 'Ventas',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 8,
            data: data.map(d => d.total),
            itemStyle: { color: chartColors.purple },
            lineStyle: { width: 3, color: chartColors.purple },
            areaStyle: {
                color: {
                    type: 'linear',
                    x: 0, y: 0, x2: 0, y2: 1,
                    colorStops: [
                        { offset: 0, color: 'rgba(139, 92, 246, 0.4)' },
                        { offset: 1, color: 'rgba(139, 92, 246, 0.05)' }
                    ]
                }
            }
        }]
    };
    
    chart.setOption(option);
}

/**
 * Gráfica de Productos por Categoría (Donut/Pie)
 */
function initProductosCategoriaChart(data) {
    const container = document.getElementById('productos-categoria-chart');
    if (!container) return;
    
    if (data.length === 0) {
        showNoDataMessage(container, 'No hay categorías registradas');
        return;
    }
    
    const chart = echarts.init(container);
    charts['productos-categoria'] = chart;
    
    const option = {
        ...darkTheme,
        tooltip: {
            ...darkTheme.tooltip,
            trigger: 'item',
            formatter: '{b}: {c} productos ({d}%)'
        },
        legend: {
            orient: 'vertical',
            right: '5%',
            top: 'center',
            textStyle: { color: '#9ca3af', fontSize: 11 },
            formatter: name => name.length > 12 ? name.substring(0, 12) + '...' : name
        },
        series: [{
            name: 'Productos',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['35%', '50%'],
            avoidLabelOverlap: true,
            itemStyle: {
                borderRadius: 6,
                borderColor: '#1e1e2e',
                borderWidth: 2
            },
            label: { show: false },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 14,
                    fontWeight: 'bold',
                    color: '#e0e0e0'
                },
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            },
            labelLine: { show: false },
            data: data.map((d, i) => ({
                value: d.cantidad,
                name: d.categoria,
                itemStyle: { color: colorPalette[i % colorPalette.length] }
            }))
        }]
    };
    
    chart.setOption(option);
}

/**
 * Gráfica de Top Productos Vendidos (Barras Horizontales)
 */
function initTopProductosChart(data) {
    const container = document.getElementById('top-productos-chart');
    if (!container) return;
    
    if (data.length === 0) {
        showNoDataMessage(container, 'No hay ventas registradas aún');
        return;
    }
    
    const chart = echarts.init(container);
    charts['top-productos'] = chart;
    
    // Invertir para que el #1 esté arriba
    const reversedData = [...data].reverse();
    
    const option = {
        ...darkTheme,
        tooltip: {
            ...darkTheme.tooltip,
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            formatter: function(params) {
                const d = params[0];
                const idx = reversedData.length - 1 - d.dataIndex;
                const original = data[idx];
                return `<strong>${d.name}</strong><br/>
                        <span style="color:${chartColors.green}">●</span> Vendido: ${d.value} unidades<br/>
                        <span style="color:${chartColors.yellow}">●</span> Ingresos: $${original.ingresos.toLocaleString('es-MX', {minimumFractionDigits: 2})}`;
            }
        },
        grid: {
            left: '3%',
            right: '10%',
            bottom: '3%',
            top: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: '#4b5563' } },
            axisLabel: { color: '#9ca3af' },
            splitLine: { lineStyle: { color: 'rgba(75, 85, 99, 0.3)' } }
        },
        yAxis: {
            type: 'category',
            data: reversedData.map(d => d.nombre.length > 20 ? d.nombre.substring(0, 20) + '...' : d.nombre),
            axisLine: { lineStyle: { color: '#4b5563' } },
            axisLabel: { color: '#9ca3af', fontSize: 11 }
        },
        series: [{
            name: 'Vendido',
            type: 'bar',
            data: reversedData.map((d, i) => ({
                value: d.vendido,
                itemStyle: {
                    color: {
                        type: 'linear',
                        x: 0, y: 0, x2: 1, y2: 0,
                        colorStops: [
                            { offset: 0, color: chartColors.green },
                            { offset: 1, color: chartColors.teal }
                        ]
                    },
                    borderRadius: [0, 4, 4, 0]
                }
            })),
            barWidth: '60%',
            label: {
                show: true,
                position: 'right',
                color: '#9ca3af',
                fontSize: 11,
                formatter: '{c}'
            }
        }]
    };
    
    chart.setOption(option);
}

/**
 * Gráfica de Stock por Categoría (Barras con valor)
 */
function initStockCategoriaChart(data) {
    const container = document.getElementById('stock-categoria-chart');
    if (!container) return;
    
    if (data.length === 0) {
        showNoDataMessage(container, 'No hay stock registrado');
        return;
    }
    
    const chart = echarts.init(container);
    charts['stock-categoria'] = chart;
    
    const option = {
        ...darkTheme,
        tooltip: {
            ...darkTheme.tooltip,
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            formatter: function(params) {
                const stockData = params[0];
                const valorData = params[1];
                return `<strong>${stockData.name}</strong><br/>
                        <span style="color:${chartColors.cyan}">●</span> Stock: ${stockData.value} unidades<br/>
                        <span style="color:${chartColors.pink}">●</span> Valor: $${valorData.value.toLocaleString('es-MX', {minimumFractionDigits: 2})}`;
            }
        },
        legend: {
            data: ['Stock', 'Valor ($)'],
            textStyle: { color: '#9ca3af' },
            top: 0
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            top: '15%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.map(d => d.categoria.length > 10 ? d.categoria.substring(0, 10) + '...' : d.categoria),
            axisLine: { lineStyle: { color: '#4b5563' } },
            axisLabel: { 
                color: '#9ca3af', 
                rotate: 30,
                fontSize: 10
            }
        },
        yAxis: [
            {
                type: 'value',
                name: 'Stock',
                position: 'left',
                axisLine: { lineStyle: { color: chartColors.cyan } },
                axisLabel: { color: '#9ca3af' },
                splitLine: { lineStyle: { color: 'rgba(75, 85, 99, 0.3)' } }
            },
            {
                type: 'value',
                name: 'Valor',
                position: 'right',
                axisLine: { lineStyle: { color: chartColors.pink } },
                axisLabel: { 
                    color: '#9ca3af',
                    formatter: v => '$' + (v / 1000).toFixed(0) + 'k'
                },
                splitLine: { show: false }
            }
        ],
        series: [
            {
                name: 'Stock',
                type: 'bar',
                data: data.map(d => d.stock),
                itemStyle: {
                    color: {
                        type: 'linear',
                        x: 0, y: 0, x2: 0, y2: 1,
                        colorStops: [
                            { offset: 0, color: chartColors.cyan },
                            { offset: 1, color: 'rgba(6, 182, 212, 0.3)' }
                        ]
                    },
                    borderRadius: [4, 4, 0, 0]
                },
                barWidth: '35%'
            },
            {
                name: 'Valor ($)',
                type: 'line',
                yAxisIndex: 1,
                data: data.map(d => d.valor),
                smooth: true,
                symbol: 'circle',
                symbolSize: 6,
                itemStyle: { color: chartColors.pink },
                lineStyle: { width: 2, color: chartColors.pink }
            }
        ]
    };
    
    chart.setOption(option);
}

/**
 * Muestra mensaje cuando no hay datos
 */
function showNoDataMessage(container, message) {
    container.innerHTML = `
        <div class="chart-no-data">
            <i class="fas fa-chart-bar"></i>
            <p>${message}</p>
        </div>
    `;
}

/**
 * Función para actualizar datos de las gráficas (para uso futuro con AJAX)
 */
function refreshCharts() {
    fetch('/api/dashboard/charts/')
        .then(response => response.json())
        .then(data => {
            initializeCharts(data);
        })
        .catch(error => {
            console.error('Error actualizando gráficas:', error);
        });
}

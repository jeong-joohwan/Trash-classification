/*** realtime. 도넛차트 값+애니메이션
 * tooltip : 마우스오버 했을 때 나오는 값 ***/

/*** 금속 도넛차트 ***/
	$(document).ready(function() {
		info = new Highcharts.Chart({
			chart: {
				renderTo: 'metal',
				margin: [0, 0, 0, 0],
				backgroundColor: null,
                plotBackgroundColor: 'none',
							
			},
			
			title: {
				text: null
			},

			tooltip: {
				formatter: function() { 
					return this.point.name +': '+ this.y +' %';
						
				} 	
			},
		    series: [
				{
				borderWidth: 2,
				borderColor: '#F1F3EB',
				shadow: false,	
				type: 'pie',
				name: 'Income',
				innerSize: '65%',
				data: [
					{ name: '금속', y: 65.0, color: '#b2c831' },
					{ name: 'rest', y: 45.0, color: '#3d3d3d' }
				],
				dataLabels: {
					enabled: false,
					color: '#000000',
					connectorColor: '#000000'
				}
			}]
		});
		
	});

/*** 유리 도넛차트 ***/

	$(document).ready(function() {
		info = new Highcharts.Chart({
			chart: {
				renderTo: 'glass',
				margin: [0, 0, 0, 0],
				backgroundColor: null,
                plotBackgroundColor: 'none',
							
			},
			
			title: {
				text: null
			},

			tooltip: {
				formatter: function() { 
					return this.point.name +': '+ this.y +' %';
						
				} 	
			},
		    series: [
				{
				borderWidth: 2,
				borderColor: '#F1F3EB',
				shadow: false,	
				type: 'pie',
				name: 'SiteInfo',
				innerSize: '65%',
				data: [
					{ name: '유리', y: 80.0, color: '#b428b4' },
					{ name: 'Rest', y: 20.0, color: '#3d3d3d' }
				],
				dataLabels: {
					enabled: false,
					color: '#000000',
					connectorColor: '#000000'
				}
			}]
		});
		
	});


/*** 플라스틱 도넛차트 ***/
	$(document).ready(function() {
		info = new Highcharts.Chart({
			chart: {
				renderTo: 'plastic',
				margin: [0, 0, 0, 0],
				backgroundColor: null,
                plotBackgroundColor: 'none',
							
			},
			
			title: {
				text: null
			},

			tooltip: {
				formatter: function() { 
					return this.point.name +': '+ this.y +' %';
						
				} 	
			},
		    series: [
				{
				borderWidth: 2,
				borderColor: '#F1F3EB',
				shadow: false,	
				type: 'pie',
				name: 'SiteInfo',
				innerSize: '65%',
				data: [
					{ name: 'Used', y: 70.0, color: '#fa1d2d' },
					{ name: 'Rest', y: 30.0, color: '#3d3d3d' }
				],
				dataLabels: {
					enabled: false,
					color: '#000000',
					connectorColor: '#000000'
				}
			}]
		});
		
	});


/*** 2차분류 도넛차트  ***/
$(document).ready(function() {
	info = new Highcharts.Chart({
		chart: {
			renderTo: 'second',
			margin: [0, 0, 0, 0],
			backgroundColor: null,
			plotBackgroundColor: 'none',
						
		},
		
		title: {
			text: null
		},

		tooltip: {
			formatter: function() { 
				return this.point.name +': '+ this.y +' %';
					
			} 	
		},
		series: [
			{
			borderWidth: 2,
			borderColor: '#F1F3EB',
			shadow: false,	
			type: 'pie',
			name: 'SiteInfo',
			innerSize: '65%',
			data: [
				{ name: 'Used', y: 45.0, color: '#0000FF' },
				{ name: 'Rest', y: 55.0, color: '#3d3d3d' }
			],
			dataLabels: {
				enabled: false,
				color: '#000000',
				connectorColor: '#000000'
			}
		}]
	});
	
});

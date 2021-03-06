
var map, osm_layer, vector_layer, point_layer;
var epsg_4326, epsg_900913;
var proj_opts;
var features_data;
var features = [];
var selected_f;
var url;
var s_style, t_style, m_style;
var selectctrl, selectpointctrl;
      
function init(){
	epsg_4326 = new OpenLayers.Projection("EPSG:4326");
	epsg_900913 = new OpenLayers.Projection("EPSG:900913");
	proj_opts = {
		'internalProjection': epsg_900913,
		'externalProjection': epsg_4326
	};

	map = new OpenLayers.Map('map');

	//OpenLayers.Feature.Vector.style['default']['strokeWidth'] = '2';

	osm_layer = new OpenLayers.Layer.OSM("OpenLayers OSM");
	var defaultstyle = new OpenLayers.Style({strokeColor:"#000000", strokeWidth:2, strokeOpacity:1});
	var tempstyle = new OpenLayers.Style({strokeColor:"#0000ff", strokeWidth:3, strokOpacity:1.0});
	var selectstyle = new OpenLayers.Style({strokeColor:"#0000ff", strokeWidth:3, strokOpacity:1.0});
	vector_layer = new OpenLayers.Layer.Vector("routelayer", {styleMap: new OpenLayers.StyleMap({'default':defaultstyle, 'temporary':tempstyle, 'select':selectstyle})});
	point_layer = new OpenLayers.Layer.Vector("pointlayer");
	
	map.addLayers([osm_layer, vector_layer, point_layer]);
	
	//map.addLayers([osm_layer, vector_layer]);

	var highlightctrl = new OpenLayers.Control.SelectFeature(vector_layer, {hover:true, highlightOnly:true, renderIntent:"temporary"});
    selectctrl = new OpenLayers.Control.SelectFeature(vector_layer, {onSelect:on_select});
	selectpointctrl = new OpenLayers.Control.SelectFeature(point_layer, {onSelect:on_select_point});

	map.addControl(highlightctrl);
	map.addControl(selectctrl);
	map.addControl(selectpointctrl);

	highlightctrl.activate();

	map.addControl(new OpenLayers.Control.MousePosition({displayProjection:epsg_4326}));

	map.setCenter(new OpenLayers.LonLat(12953390, 4848000), 11);

	t_style = {
                strokeColor: "#00FF00",
				strokOpacity: 1,
				fillColor: "#00ff00",
				fillOpacity: 0.5,
                pointRadius: 5,
            };

	s_style = {
                strokeColor: "#FF0000",
				strokOpacity: 1,
				fillColor: "#FF0000",
				fillOpacity: 0.5,
                pointRadius: 5,
            };
	m_style = {
                strokeColor: "#0000ff",
				strokOpacity: 1,
				fillColor: "#0000ff",
				fillOpacity: 0.3,
                pointRadius: 5,
            };
}

function get_track_data(filename) {
	if (filename) {
		url = "../data/tracks/" + filename;
		if(!url.match(/json$/)){
			str = url + ".json";		
		}
		$.ajax({
			url: url,
  			success: plot_track,
			error: info_error
		});
	}
}

function plot_track(jsondata) {
	if(!is_hold_on()){	
		features = [];
	}
	vector_layer.removeAllFeatures();
	point_layer.removeAllFeatures();
	selectctrl.activate();

	//features_data = jsondata;
	var geojsoner = new OpenLayers.Format.GeoJSON(proj_opts);
	var tmp_fs = geojsoner.read(jsondata);
	if(tmp_fs) {
		if(tmp_fs.constructor != Array) {
			tmp_fs = [tmp_fs];
		}
		features = features.concat(tmp_fs);
        vector_layer.addFeatures(features);
	}else{
		alert(url + " is broken");
	}
}

function replot_track() {
	vector_layer.removeAllFeatures();
	point_layer.removeAllFeatures();
	selectctrl.activate();
	vector_layer.addFeatures(features);
	selectctrl.unselect(selected_f);
}

function on_select(feature){
	vector_layer.removeAllFeatures();
	vector_layer.addFeatures([feature]);
	selected_f = feature;

	var mapinfo_tb = clear_mapinfo_tb();

	var lonlats = feature.geometry.clone().transform(epsg_900913, epsg_4326).getVertices();
	var lonlats2 = feature.geometry.getVertices();

	var pnum = lonlats2.length;
	var points = [];

	for(var i=1; i < pnum-1; i++){
		points.push(new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonlats2[i].x, lonlats2[i].y), null, m_style));	
	}
	points.push(new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonlats2[0].x, lonlats2[0].y), null, s_style));	
	points.push(new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonlats2[pnum-1].x, lonlats2[pnum-1].y), null, t_style));	
	point_layer.addFeatures(points);

	if (typeof feature.attributes.desc != 'undefined'){
		var dnum = feature.attributes.desc.length;
		for(var i=0; i < dnum; i++){
			mapinfo_tb.last().append('<tr>' + 
									  '<td>' + lonlats[i].x.toFixed(8) + '</td>' +
									  '<td>' + lonlats[i].y.toFixed(8) + '</td>'+
									  '<td>' + feature.attributes.desc[i]["t"] + '</td>' +
									  '<td>' + feature.attributes.desc[i]["s"] + '</td>' +
									  '<td>' + feature.attributes.desc[i]["h"] + '</td>' +
									  '<td>' + feature.attributes.desc[i]["o"] + '</td>' + '</tr>');
		}	
	}
	selectctrl.deactivate();
	selectpointctrl.activate();	
}

function on_select_point(feature){
	lonlat = feature.geometry.clone().transform(epsg_900913, epsg_4326).getVertices();
	get_mapinfo_tb_rows().each(function() {
    	if ($(this).children(":eq(0)").text() == lonlat[0].x.toFixed(8) && $(this).children(":eq(1)").text() == lonlat[0].y.toFixed(8)){
			$(this).css({"background-color": "#aaaaaa"});
		}else{
			$(this).css({"background-color": "#ffffff"});
		}
	});
}

function info_error(e){
	alert(url + " not found");
}


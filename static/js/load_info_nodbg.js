function CreatedivWithContent()
{



}
function UnpairAll(btnobject)
{
	var ipaddr = document.getElementById("ipaddr"); 
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var responseTxt = JSON.parse(xhttp.responseText);
			let str="UnapirAll: ";
			str += responseTxt.UnPairAll;
			alert(str);
		}
	};
	var random1=Math.random();
	request="http://"  + ipaddr.innerHTML + ":" + "5001/UnpairAll?version=" + random1;
	//alert(request);
	xhttp.open("GET", request, true);
	xhttp.send();
	

}
function PairOrUnpair(userdata, btnobject)
{
	
	//alert(userdata.idxinlist+btnobject.getAttribute("innerHTML"));
	var ipaddr = document.getElementById("ipaddr"); 
//	btnobject.setAttribute("innerHTML", "Unpair");
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var responseTxt = JSON.parse(xhttp.responseText);
			let str = responseTxt.Pairing;
			alert(str);
			if(responseTxt.Pairing=="Success")
			{
				btnobject.innerHTML="Unpair";

			}
			else 
			{

				btnobject.innerHTML="Pair";

			}

		}
	};
	var request;
	var random1=Math.random();
	if(btnobject.innerHTML == "Pair")
		request="http://"  + ipaddr.innerHTML + ":" + "5001/CommissionMatterDevice?" +  "index=" + userdata.idxinlist + "&version=" + random1;
	else 		
		request="http://"  + ipaddr.innerHTML + ":" + "5001/UnpairMatterDevice?" +  "index=" + userdata.idxinlist + "&version=" + random1;
	// alert(ipaddr.innerHTML);
	//xhttp.open("GET", "http://192.168.1.63:5000/login", true);
	//alert(request);
	xhttp.open("GET", request, true);
	xhttp.send();
	
};
function UpdateDataOnPage(responseTxt1, userdata)
{
	var curstatus;
	var responseTxt;
	//try 
	{
	//	var tmp = '{{ responseTxt1 | tojson }}';
	//	var tmp = JSON.parse('{{responseTxt1|tojson|safe}}');
		responseTxt2=responseTxt1.listdata;
		//console.log(userdata)
		for(j=0; j<responseTxt2.length; j++) {
			responseTxt=responseTxt2[j];
			for(i=0; i< userdata.length; i++) {

				if(responseTxt.devicename != userdata[i].name)
					continue;
				console.log(responseTxt)
					elementid="info" + userdata[i].name;
				var infotxtnode = document.getElementById(elementid);
				if (userdata[i].type == "plug")
					if (responseTxt.CurCurrent == "Invalid" || responseTxt.CurCurrent == "0")
						curstatus="Off ";		
				infotxtnode.innerHTML= "&emsp;&emsp;&emsp;&emsp;<b>Status: </b>" + curstatus + "<br>" + "&emsp;&emsp;&emsp;&emsp;<b>Current(mA): </b>" + responseTxt.CurCurrent  + "<br>" + "&emsp;&emsp;&emsp;&emsp;<b>Voltage(V): </b>" + responseTxt.CurVoltage +  "<br>" + "&emsp;&emsp;&emsp;&emsp;<b>Power(W): </b>" +  responseTxt.CurPower + "<br>" + "&emsp;&emsp;&emsp;&emsp;<b>Electricity Usage(kWh): </b>" + responseTxt.CurPwrUsage; 
				//break;
			}

		}
	}
	//catch{console.log("something failed while parsing data stats response");}
	//catch{console.log("got some errors");}
};

function GetDeviceData(userdata)
{
	try {
		var ipaddr = document.getElementById("ipaddr"); 
		//	btnobject.setAttribute("innerHTML", "Unpair");

		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (xhttp.readyState == 4 && xhttp.status == 200) {
				var responseTxt = JSON.parse(xhttp.responseText);
				let str = responseTxt.success;
				//console.log(xhttp.responseTxt)
				console.log(responseTxt)
				UpdateDataOnPage(responseTxt, userdata)
			}
		};

		var random1=Math.random();
		var request="http://"  + ipaddr.innerHTML + ":" + "5001/devicestats?" +  "version=" + random1;
		//console.log(request);
		xhttp.open("GET", request, true);
		xhttp.send();
	}
	catch{console.log("something failed while sending data stats request");}

};
//staticurl is useledd param
function onloadfunction(var2, staticurl, devdata)
{
	try{
		var elem=document.getElementById("divdata");
		var datadiv = document.getElementById("divdata2");
		userdata = JSON.parse(var2);
		for(var i=0; i< userdata.length; i++) {
			var div1 = document.createElement("DIV");
			var textNode = document.createTextNode(userdata[i].name);
			var x = document.createElement("SPAN");
			var imgelem = document.createElement("IMG")
				var btn = document.createElement("BUTTON");
			var pairstatus = userdata[i].pairstatus;
			btn.style.display="inline-block";
			btn.setAttribute("style", "font-weight: bold; background-color: rgb(157,0,117); height: 30px; width: 100px; display: inline-block; margin-left: 50px;");
			if(pairstatus  == "paired"){
				btn.innerHTML="Unpair";
				//var tmpdataobj = "pair" + userdata[i].idxinlist;
				//btn.setAttribute("innerHTML", tmpdataobj);
				btn.setAttribute("name", "Unpair");
			}
			else {
				btn.innerHTML="Pair";
				btn.setAttribute("name", "Pair");

			}
			btn.addEventListener("click", PairOrUnpair.bind(null, userdata[i], btn));
			//imgelem.setAttribute("src", "{{ url_for('static', filename='sample_image.png') }}");
			imgelem.setAttribute("src", "/static/sample_image.png");
			div1.style.padding = "20px";
			x.style.display="block";
			x.style.width="100px";
			x.style.textAlign="center";
			x.style.fontWeight = 'bold';
			x.appendChild(textNode);
			/*
			   x.style.padding="10px";
			   imgelem.style.padding = "20px";
			 */
			div1.appendChild(imgelem);
			div1.appendChild(btn);
			div1.appendChild(x);
			elem.appendChild(div1);

			if (devdata == "ON"){
				var h3node = document.createElement('h3');
				h3node.innerHTML=userdata[i].name;
				var infotxtnode = document.createElement('p');
				infotxtnode.setAttribute('id', "info" + userdata[i].name);
				if(userdata[i].type == "bridge"){
					infotxtnode.innerHTML= "No Of Devices: " + 0;
				}	
				else if(userdata[i].type == "light")
					if(userdata[i].name != "musicplayer")
						infotxtnode.innerHTML= "Color:" + "Red " + "Brightness: " + 254 + " Status: " + "Off";
					else 
						infotxtnode.innerHTML= "Status : " + "Stopped";
				//&nbsp;&nbsp;&nbsp;&nbsp;
				else if(userdata[i].type == "plug") {	
					infotxtnode.innerHTML= "<b>&emsp;&emsp;&emsp;&emsp;Status: </b>" + "Off " + "<br>" + "  <b>&emsp;&emsp;&emsp;&emsp;Current(mA): </b>" + 254 + "<br>" + "<b>&emsp;&emsp;&emsp;&emsp;Voltage(V): </b>" + 254 +  "<br>" + "<b>&emsp;&emsp;&emsp;&emsp;Power(W): </b>" + 0 + "<br>" + "<b>&emsp;&emsp;&emsp;&emsp;Electricity Usage(kWh): </b>" + 0;
					infotxtnode.style.textAlign='left';
				}
				else if(userdata[i].type == "light switch")
					infotxtnode.innerHTML= "Status : " + "Off";

				datadiv.appendChild(h3node);
				datadiv.appendChild(infotxtnode);
			}

		}	
		elem.style.visibility='visible';
		var elem1=document.getElementById("divdata1");
		var y = document.getElementById("unpairbtn");
		y.addEventListener("click", UnpairAll.bind(null, y));
		if (devdata == "ON"){
			datadiv.style.visibility='visible';

			var TimerInst=setInterval(GetDeviceData, 15000, userdata);
		}
		else {
			datadiv.style.display = 'none'

		}
	}
	catch{console.log("onload function failed somehwere !!");}
};

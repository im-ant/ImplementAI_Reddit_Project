var isRecording = false;

 var userMedia = undefined;
    navigator.getUserMedia = navigator.getUserMedia
    || navigator.webkitGetUserMedia
    || navigator.mozGetUserMedia
    || navigator.msGetUserMedia;


if(!navigator.getUserMedia){
    console.error("No getUserMedia Support in this Browser");
}

navigator.getUserMedia({
    audio:true
}, function(stream){
    userMedia = stream;
}, function(error){
    console.error("Could not get User Media: " + error);
});

Nuance.logger = {
            log: function(msg){
                LOG(msg, 'out');
            }
        };


var recordButton = $("#recordButton");
var recordButtonIcon = $("#recordButton i").first();

var defaultOptions = {
    onopen: function() {
        console.log("Websocket Opened");
        //$content.addClass('connected');
    },
    onclose: function() {
        console.log("Websocket Closed");
        //$content.removeClass('connected');
    },
    onvolume: function(vol) {
        //viz(vol);
    },
    onresult: function(msg) {
        LOG(msg, 'in');
        console.log(msg);
        if (msg.result_type === "NMDP_TTS_CMD" || msg.result_type === "NVC_TTS_CMD") {
            //dLog(JSON.stringify(msg, null, 2), $ttsDebug);
            //$ttsGo.prop('disabled', false);
        } else if (msg.result_type === "NVC_ASR_CMD") {
            //dLog(JSON.stringify(msg, null, 2), $asrDebug);
        } else if (msg.result_type == "NDSP_ASR_APP_CMD") {
            if(msg.result_format === "nlu_interpretation_results") {
                try{
                    //dLog("interpretations = " + JSON.stringify(msg.nlu_interpretation_results.payload.interpretations, null, 2), $asrDebug);
                //alert("interpretations = " + JSON.stringify(msg.nlu_interpretation_results.payload.interpretations, null, 2));
                	var concepts = msg.nlu_interpretation_results.payload.interpretations[0];
                	if(!!concepts)
                	{
						concepts = concepts.concepts;

                		var symbol = concepts.COMPANY[0].value;
                		if(!!symbol)
                		{
	                		if(companyDataDict.hasOwnProperty(symbol))
	                		{
	                			$( "#categorySelect" ).val(reverseCategoryDict[symbol]).change();
	                			$( "#companySelect" ).val(symbol).change();
	                		}
	                		else if(symbol == "NUAN")
	                		{
	                			setTimeout(function(){tts("Nuance is not a Fortune 500 company");}, 500);
	                			console.log("Nuance is not a Fortune 500 company");
	                		}
	                		else
	                		{
	                			var msg = "We don't have data for " + concepts.COMPANY[0].literal;
	                			setTimeout(function(){tts(msg);}, 500);
	                			console.log(msg);
	                		}
                		}
                	}
                	else
                	{
                		
        			var msg = "Could you please repeat that?";
        			setTimeout(function(){tts(msg);}, 500);
        			console.log(msg);
                	}
                }catch(ex){
                    //dLog(JSON.stringify(msg, null, 2), $asrDebug, true);
                    //alert("exception:\n" + JSON.stringify(msg, null, 2));
        			var msg = "Could you please repeat that?";
        			setTimeout(function(){tts(msg);}, 500);
        			console.log(msg);
                }
            } else {
                //dLog(JSON.stringify(msg, null, 2), $asrDebug);
            }
            //recordButton.prop('disabled', false);
        } else if (msg.result_type === "NDSP_APP_CMD") {
            if(msg.result_format === "nlu_interpretation_results") {
                try{
                    //dLog("interpretations = " + JSON.stringify(msg.nlu_interpretation_results.payload.interpretations, null, 2), $nluDebug);
                }catch(ex){
                    //dLog(JSON.stringify(msg, null, 2), $nluDebug, true);
                }
            } else {
                //dLog(JSON.stringify(msg, null, 2), $nluDebug);
            }
            //$nluExecute.prop('disabled', false);
        }
    },
    onerror: function(error) {
        LOG(error);
        console.error(error);
        //$content.removeClass('connected');
        //$recordButton.prop('disabled', false);
    }
};

function createOptions(overrides) {
    var options = Object.assign(overrides, defaultOptions);
    options.appId = APP_ID;
    options.appKey = APP_KEY;
    options.userId = USER_ID;
    options.url = URL;
    return options;
}

// Text NLU

function textNlu(evt){
    var options = createOptions({
        text: $("#nlu_text").val(),
        tag: NLU_TAG,
        language: ASR_LANGUAGE
    });
    //$nluExecute.prop('disabled', true);
    Nuance.startTextNLU(options);
}
//$nluExecute.on('click', textNlu);

// ASR / NLU

function asr(evt){
    console.log("button clicked");
    if(isRecording) {
        Nuance.stopASR();
        //$asrLabel.text('RECORD');
        recordButtonIcon.addClass("fa-microphone");
        recordButtonIcon.removeClass("fa-microphone-slash");
    } else {
        //cleanViz();
        var options = createOptions({
            userMedia: userMedia,
            language: ASR_LANGUAGE
        });

        options.nlu = true;
        options.tag = NLU_TAG;
        Nuance.startASR(options);
        recordButtonIcon.addClass("fa-microphone-slash");
        recordButtonIcon.removeClass("fa-microphone");
    }
    isRecording = !isRecording;
}
recordButton.on('click', asr);

// TTS

function tts(textToSay){
    var options = createOptions({
        language: ASR_LANGUAGE,
        voice: TTS_VOICE,
        text: textToSay
    });
    //$ttsGo.prop('disabled', true);
    Nuance.playTTS(options);
}
//$ttsGo.on('click', tts);


var LOG = function LOG(msg, type){
        var html = "<pre>"+JSON.stringify(msg, null, 2)+"</pre>";
        var time = new Date().toISOString();
        if(type === 'in'){
            html = '<span class="label label-info"><<<< Incoming (' + time + ')</span>' + html;
        } else {
            html = '<span class="label label-primary">>>>> Outgoing (' + time + ')</span>' + html;
        }
        console.log(html);
};
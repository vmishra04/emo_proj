$(document).ready(function() {
    console.log("hola")
    $('#save-mod-first').click(function(){
        new_text = $('#first-message-mod').val();
        console.log(new_text);
        $('#first-message-title').text(new_text);
    });
    
    $('#save-mod-pos').click(function(){
        new_text = $('#pos-mod').val();
        console.log(new_text);
        $('#pos').text(new_text);
    });
    
    $('#save-mod-neg').click(function(){
        new_text = $('#neg-mod').val();
        console.log(new_text);
        $('#neg').text(new_text);
    });
});

$(window).on("load",function() {
    $('#sendSMS').click(function(){
        console.log('Hola')
        option = $("input[name=gender]:checked").val();
        console.log(option);
        text = $('#first-message-title').text();
        new_text = text.replace("<productType>",option)
        console.log(new_text);
        $('#first-message-title').text(new_text);
    });
});
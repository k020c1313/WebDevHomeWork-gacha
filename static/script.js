var srpCount= $('#srpcount').children().length

console.log(srpCount)

if (srpCount === 10){
    console.log($('#srpcount').length)
    
    $("#ren10-button").prop("disabled", true);
    $("#ren1-button").prop("disabled", true);
    $("#complete-button").prop("disabled", true);
    
    setTimeout(function(){
    alert("SR+が全種類揃いました！\n続行するにはリセットボタンを押してください。")
        }, 500);
}

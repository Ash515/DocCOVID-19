function gresult(){
var a=document.getElementById('docres').value;
var b=document.getElementById('mlres').value;
if (a===b){
    document.getElementById('textarea').value="yes";
}else{
    
    document.getElementById('textarea').value="No";
}
}


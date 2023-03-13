const barCanvas=document.getElementById(barCanvas);
const barChart= new Chart(barCanvas,{
    type:"bar",
    data:{
        labels:["HGOPY","CURY","ST JOSEPH"],
        datasets:[{
            data:[12,14,3],
        }]
    }
})
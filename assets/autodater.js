function GetDays(){
                var dropdt = new Date(document.getElementById("drop_date").value);
                var pickdt = new Date(document.getElementById("pick_date").value);
                return parseInt((dropdt - pickdt) / (24 * 3600 * 1000));
        }

        function cal(){
        if(document.getElementById("drop_date")){
            document.getElementById("numdays2").value=GetDays();
        }  
    }
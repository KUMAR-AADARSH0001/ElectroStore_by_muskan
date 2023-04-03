
function myfun(e){
    prid = e;
    $.ajax({
        url:'{% url "index" %}',
        type:'get',
        data:{prid:prid},
        success:function(data){
            var check = (data.description).search('@');
            if(check==-1){
                dsc = data.description;
            }
            else{
                var dd = (data.description).split('@');
                dsc = '';
                for(var i=0; i<dd.length-1;i++){
                    dsc+='<li>'+dd[i]+'</li>';
                }
            }
            $('.pimg').html('<img src="/media/'+data.photo+'" alt="No Image" class="img-responsive" height="100%"/>');
            $('#pname').html(data.name);
            $('#pdes').html('<ul>'+dsc+'</ul>');
            $('#pp').html(data.price);
            $('#sp').html(data.sale_price); 
            $('#iprice').val(data.sale_price);
            $('#pn').val(data.name);
        }
    });
}

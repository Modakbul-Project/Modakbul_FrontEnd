<script>
  var x,y;
  $(function(){
       var socket = io.connect('http://' + document.domain + ':' + location.port);

      socket.on( 'connect', function() {
        socket.emit( 'postit', {
          data: 'cnt'
        } )

        $("button").on("click",function(e){
            makedrag();
        });
        //저장 내용물 - 좌표/메시지/텍스트에리어 사이즈
      });

    //불러오기
    socket.on( 'postitres', function( msg ) {
        if( typeof msg.id !== 'undefined' ) {
            if(msg.user != "{{user}}"){
                console.log("이동");
                makememo(msg.id,msg.x,msg.y,msg.message);
            }
        }
      })
  });

  function resize(area){
        area.style.height = 'auto';
        let height = area.scrollHeight; // 높이
        area.style.height = `${height}px`;
    }

    function makedrag(id,posx,posy,message){
        if(id == undefined){id='None'}
        $("<div class='draggable' id='"+id+"' style='top:"+posy+"px; left:"+posx+"px;'><textarea name='sticky' id='' placeholder='memo here'>"+message+"</textarea></div>").appendTo("#board").draggable({containment:'#board'}).on("mouseup" ,function(e){
          x = $(this).position().left;
          y = $(this).position().top;
          message = $(this).children($('textarea')).val();

            socket.emit( 'postit', {
                id : id,
                x : x,
                y : y,
                message : message,
              } )

              $(this).children($('textarea')).on('keyup', function(){
                     resize(this);
                     //소켓 저장
                    // socket.emit('postit',{
                    //    message = $(this).children($('textarea')).val();
                    // })
              });
        }, 'keydown' : function(){

            socket.emit( 'postit', {
                    id : id,
                    x : x,
                    y : y,
                    message : message,
            } )
          var newpost = $(this);
          socket.on( 'newpostit', function( msg ) {
             if(msg.user == "{{user}}"){
                //this에 id값 추가해줌
                id = msg.id
                newpost.attr('id',msg.id);
                console.log(newpost.attr('id'));
             }
         })
         console.log(id, x,y, message);

        });
    }

    function makememo(id,x,y,message){
        console.log(id, x,y,message);
        if($("#"+id).length>0){
            $("#"+id).css({"top" : y, "left" : x});
            $("#"+id).children($('p')).html(message);
        }else{
            $("<div class='memo' id='"+id+"'><p>"+message+"</p></div>").appendTo("#board").css({"top" : y, "left" : x});
        }
    }




</script>
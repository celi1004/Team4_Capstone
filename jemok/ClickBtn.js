window.onload = function(){
  var key_btn = window.document.getElementsByName('keyword');

  if(key_btn){
    $("a[name=keyword]").each(function(index, item){
      $(item).click(function(){
        KeywordClicked($(item).attr('id'));
      });
    });
  }

  var changebtn = window.document.getElementById('changeBtn');
  var rechangebtn = window.document.getElementById('rechangeBtn');

  if(changebtn){
    changebtn.addEventListener('click', () =>{
        changeBtn_click();
    });
  }
  invalid_rechange();

  chrome.runtime.onMessage.addListener( function(message, sender, sendResponse) {
    console.log(message);
    if(message == "false"){
      setTimeout(()=>{
        invalid_rechange();
        sendResponse("invalid_rechange");
      }, 500);
      return true;
  	}
    else if(message == "true"){
      setTimeout(() =>{
        valid_rechange();
        sendResponse("valid_rechange");
      }, 500);
      return true;
    }
    else if(!(message == "false" || message == "true" || message == "changeFinished" || message == "FailtoFinish")){
      console.log(message);
      invalid_keywordByCate(String(message));
    }
  });
}

var keyword_name = ['상품명', '브랜드', '가격', '상태', '색상', '거래방식', '착용횟수', '사이즈', '용량', '사양', '사용기간']
var keyword_elem = [{name:'상품명', categorie:'공통', selected:false}, {name:'브랜드', categorie:'공통',selected:false}, {name:'가격', categorie:'공통', selected:false}, {name:'상태', categorie:'공통', selected:false}, {name:'색상', categorie:'공통', selected:false}, {name:'거래방식', categorie:'공통', selected:false}, {name:'착용횟수', categorie:'의류', selected:false}, {name:'사이즈', categorie:'의류', selected:false}, {name:'용량', categorie:'IT/전자기기', selected:false}, {name:'사양', categorie:'IT/전자기기', selected:false}, {name:'사용기간', categorie:'IT/전자기기', selected:false} ]
var keyword_list = []
var selected_categorie = {'공통': {n:0}, '의류': {n:0}, 'IT/전자기기': {n:0}}
for(let i=0; i<keyword_name.length; i++){
  var key = keyword_name[i];
  keyword_list[key] = keyword_elem[i];
}
var categorie = {clothes: [ "여성상의", "여성하의", "여성신발", "남성상의", "남성하의", "남성신발", "가방/모자/장갑", "지갑/벨트/시계", "안경/선글라스", "기타패션잡화", "학생교복", "파티/잠옷/작업복등"], phone: ["SKT", "KT", "LGU+", "기타통신사/피처폰", "주변기기/악세사리"], it :["노트북/맥북/넷북", "태블릿PC", "데스크탑/본체", "모니터", "CPU/메인보드/RAM", "HDD/SSD/ODD/USB", "VGA/SOUND", "케이스/파워/쿨러", "키보드/마우스/스피커", "프린터/잉크/토너", "공유기/랜카드/케이블", "PC게임/소프트웨어", "기타컴퓨터용품"]}

function invalid_rechange(){
  var tmp = $('#rechangeBtn');
  tmp.css("background-color","#D5D5D5");
  tmp.css("border", "2px solid #D5D5D5");
  tmp.removeClass('change_Btn');
  tmp.unbind();
}

function valid_rechange(){
  var tmp = $('#rechangeBtn');
  tmp.css("background-color", "#32B2B2");
  tmp.css("border", "2px solid #32B2B2");
  tmp.addClass('change_Btn');
  tmp.unbind();
  tmp.bind('click', rechangeBtn_click);
}

function invalid_keywordByCate(cate){

  var clothes = categorie.clothes;
  var phone = categorie.phone;
  var it = categorie.it;
  if(clothes.indexOf(cate) != -1 || cate.indexOf("명품") != -1){
    for(let i=0; i<keyword_elem.length; i++){
      if(keyword_elem[i].categorie == 'IT/전자기기'){
        var btn = $("a#"+keyword_elem[i].name);
        btn.css("background-color","#D5D5D5");
        btn.removeClass('btn');
        btn.unbind();
        deleteKeyword(keyword_elem[i].name, false);
      }
     else{
       var btn = $("a#"+keyword_elem[i].name)
       var ak = $("#added_keyword_"+keyword_elem[i].name).length;
       if(ak>0){
          console.log("dd"+keyword_elem[i].name)
          if(btn.css("background-color")=="#D5D5D5"){
            btn.css("background-color","rgba(221,205,34, 0.2)");
          }
       }
       else{
         console.log(keyword_elem[i].name)
         btn.css("background-color","rgba(0,180,204,0.15)");
       }
       btn.addClass('btn');
       btn.unbind();
       btn.click(function(){
         KeywordClicked(keyword_elem[i].name);
       });
     }
    }
  }
  else if(phone.indexOf(cate) != -1){
    for(let i=0; i<keyword_elem.length; i++){
      if(keyword_elem[i].categorie == '의류'){
        var btn = $("a#"+keyword_elem[i].name)
        btn.css("background-color","#D5D5D5");
        btn.removeClass('btn');
        btn.unbind();
        deleteKeyword(keyword_elem[i].name, false);
      }
     else{
       var btn = $("a#"+keyword_elem[i].name)
       var ak = $("#added_keyword_"+keyword_elem[i].name).length;
       if(ak>0){
          console.log("dd"+keyword_elem[i].name);
          if(btn.css("background-color")=="#D5D5D5"){
            btn.css("background-color","rgba(221,205,34, 0.2)");
          }
       }
       else{
         console.log(keyword_elem[i].name)
         btn.css("background-color","rgba(0,180,204,0.15)");
       }
       btn.addClass('btn');
       btn.unbind();
       btn.click(function(){
         KeywordClicked(keyword_elem[i].name);
       });
     }
    }
    var btn = $("a#사양")
    btn.css("background-color","#D5D5D5");
    btn.removeClass('btn');
    btn.unbind();
    deleteKeyword("사양", false);
  }
  else if(it.indexOf(cate) != -1){
    for(let i=0; i<keyword_elem.length; i++){
      if(keyword_elem[i].categorie == '의류'){
        var btn = $("a#"+keyword_elem[i].name)
        btn.css("background-color","#D5D5D5");
        btn.removeClass('btn');
        btn.unbind();
        deleteKeyword(keyword_elem[i].name, false);
      }
     else{
       var btn = $("a#"+keyword_elem[i].name);
       var ak = $("#added_keyword_"+keyword_elem[i].name).length;
       if(ak>0){
         console.log("dd"+keyword_elem[i].name);
         if(btn.css("background-color")=="#D5D5D5"){
           btn.css("background-color","rgba(221,205,34, 0.2)");
         }
       }
       else{
         console.log(keyword_elem[i].name)
         btn.css("background-color","rgba(0,180,204,0.15)");
       }
       btn.addClass('btn');
       btn.unbind();
       btn.click(function(){
         KeywordClicked(keyword_elem[i].name);
       });
     }
    }
  }
  else{
    for(let i=0; i<keyword_elem.length; i++){
      if(keyword_elem[i].categorie == '공통'){
        var btn = $("a#"+keyword_elem[i].name);
        var ak = $("#added_keyword_"+keyword_elem[i].name).length;
        if(ak>0){
          console.log("dd"+keyword_elem[i].name);
          if(btn.css("background-color")=="#D5D5D5"){
            btn.css("background-color","rgba(221,205,34, 0.2)");
          }
        }
        else{
          console.log(keyword_elem[i].name)
          btn.css("background-color","rgba(0,180,204,0.15)");
        }
        btn.addClass('btn');
        btn.unbind();
        btn.click(function(){
          KeywordClicked(keyword_elem[i].name);
        });
      }
      else{
        var btn = $("a#"+keyword_elem[i].name)
        btn.css("background-color","#D5D5D5");
        btn.removeClass('btn');
        btn.unbind();
        btn.click(function(){
          alert("공통/선택된 카테고리 안 키워드에 대해서만 선택 가능합니다.");
        });
        deleteKeyword(keyword_elem[i].name, false);
      }
    }
  }
}

function KeywordClicked(s){

  if(keyword_list[s].selected==false){
    addKeyword(s);
  }
  else{
    deleteKeyword(s, true);
  }
}

function addKeyword(s){

  //버튼 추가
  var addFormDiv = document.getElementById("addedKeywordForm");

  var str = ['<span class="btn" herf="#">',
              '<p class="addedKeyword">'+s+'</p>',
              '<p class="del_keyword" id="del_keyword_'+s+'">&nbsp;&nbsp;&Cross;</p>',
            '</span>'].join('\n');

  var addedDiv = document.createElement("li");
  addedDiv.setAttribute("id", "added_keyword_"+s);
  addedDiv.innerHTML = str;
  addFormDiv.appendChild(addedDiv);

  if(keyword_list[s].categorie == '의류'){
    selected_categorie['의류'].n++;
  }
  else if(keyword_list[s].categorie == 'IT/전자기기'){
    selected_categorie['IT/전자기기'].n++;
  }
  //추가됐다 표시
  if(keyword_list[s].selected==false){
    keyword_list[s].selected = true;
  }

  //키워드버튼 플러스 엑스로 바꾸고 색 바꿈
  var clicked_btn = document.getElementById(s);
  var str1 = ['<i class="fab">'+s+'</i>',
              '<i class="fab">x</i>'].join('\n');
  clicked_btn.innerHTML = str1;
  clicked_btn.style.backgroundColor = "rgba(221,205,34, 0.2)";

  //추가키워드 삭제 이벤트 등록
  var delBtn = document.getElementById("del_keyword_"+s);
  delBtn.addEventListener('click', () =>{
    deleteKeyword(s, true);
  });

  //키워드 추가 때 마다 드래그이벤트 호출
  keywordDrag();

}

function deleteKeyword(s, yn){
  var delFormLi = document.getElementById("added_keyword_"+s);

  if(delFormLi){
    while(delFormLi.firstChild){
      delFormLi.removeChild(delFormLi.firstChild);
    }
    delFormLi.remove();
    if(keyword_list[s].selected == true){
      keyword_list[s].selected = false;
    }
  }

    var clicked_btn = document.getElementById(s);
    if(clicked_btn){
      var str1 = ['<i class="fab">'+s+'</i>',
                '<i class="fab">+</i>'].join('\n');
      clicked_btn.innerHTML = str1;
    }
  if(yn == true){
    clicked_btn.style.backgroundColor = "rgba(0,180,204,0.15)";
  }
}

function keywordDrag(){
  $("ul#addedKeywordForm").sortable({
    placeholder: "placeholder",
    item:"span",
    connectwith:"ul#addedKeywordForm",
    toleracneElement:"> p",
    handle: "p",
    cursor:"move",
    axis: "x",
    update: function(event, ui){
    }
  }).disableSelection();
}

function changeBtn_click(){

  var addedKeyword_list = []
  $(".addedKeyword").each(function(index, item){
    addedKeyword_list[index] = $(item).text();
  });

  if(addedKeyword_list.length == 0){
    alert("키워드를 선택해주세요.");
    return;
  }

    alert("게시물 제목을 <"+addedKeyword_list+">에 대해 변경합니다.");
    loading();

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var keyword = JSON.stringify(addedKeyword_list);
      console.log(keyword);
      chrome.tabs.sendMessage(tabs[0].id, {msg: "change", keyword:keyword}, function(response) {
      });
    });
  // 변경 완료 시 이벤트
    chrome.runtime.onMessage.addListener( function(message, sender, sendResponse) {
      if(message == "changeFinished"){
        closeLoading();
        whale.sidebarAction.hide(function(){

        });
      }
      else if(message == "FailtoFinish"){
        closeLoading();
        console.log("서버 요청에 실패하였습니다.")
      }
    });
}

function rechangeBtn_click(){
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {msg: "rechange"}, function(response) {
      console.log("sendMessage rechange");
    });
  });
}

function loading(){

  var maskHeight = $(document).height();
  var maskWidth = window.document.body.clientWidth;

  var mask = "<div id='mask' style='position:absolute; z-index:9000; background-color:#000000; display:none; left:0; top:0;'></div>";
  var loadingImg = '';

  loadingImg = "<img src='images/loadingImage.gif' style='position: absolute; left:25%; top:35%; display: block; margin: 0px auto;'/>";

  $('body').append(mask)

  $('#mask').css({
    'width': maskWidth,
    'height': maskHeight,
    'opacity': '0.13'
  });

  $('#mask').show();

  $('#loadingImg').append(loadingImg);
  $('#loadingImg').show();
}

function closeLoading(){
  $('#mask, #loadingImg').hide();
  $('#mask, #loadingImg').empty();
}

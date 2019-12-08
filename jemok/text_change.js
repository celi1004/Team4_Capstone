var test_data = {654912086:{title:'롱패딩		|		?		|		9000		|		M		'}, 646926413:{title:'하프 집업 집업 니트		|		?		|		49000		|		M		'}, 642716194:{title:'싱글 코트		|		?		|		80000		|		?		'}, 626446408:{title:'라이더 자켓		|		?		|		130000		|		M		'},623635707:{title:'?		|		?		|		23000		|		?		'},606055089:{title:'	자켓		|		?		|		90000		|		?		'}, 618993083:{title:'자켓 패딩		|		닥스		|		70만원		|		100		'}, 616581663:{title:'네		|		?		|		210000		|		?		'}, 615476511:{title:'베이지		|		파타고니아		|		150000		|		L		'}, 614007547:{title:'제목j'}, 606060821:{title:'제목k'},591452350:{title:'제목l'},578529315:{title:'제목m'}, 506082774:{title:'제목n'},503003663:{title:'제목o'}}
var was_changed = false;
var is_changed = false;
var doit = 0;
$('head').append('<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests"> ');
if(document.body.innerHTML.search('main-area') != -1) {
	console.log('target frame!');

	var categorie = $('.sub-tit-color').text();

	if(categorie == '사전예약하고 카페 가입하기' || !categorie){
		categorie = $('#currentSearchMenuTop').text();
	}
	chrome.runtime.sendMessage(categorie, response =>{
		console.log(response);
	});

	var table = document.getElementsByClassName('article-board')[1];

	if(table){
		var title_number = table.getElementsByClassName('inner_number');
		var title_list = table.getElementsByClassName('article');
		var numoftitle = title_list.length;

		var article_num = []
		var forChange = {}
		for(let i=0; i<numoftitle; i++){
			article_num.push( title_number[i].innerText );
			forChange[title_number[i]] = i;
			localStorage.setItem(article_num[i], title_list[i].innerText);
		}

		var crawling_result = []
		var src_url = "https://m.cafe.naver.com/joonggonara";
		for(let i=0; i<title_list.length; i++){
			var tmp_url = title_list[i].getAttribute('href')
			var tmp_number = title_number[i].innerText;
			var jqshr = $.get(src_url+tmp_url, function(data){
				var num = data.indexOf("article_id");
				var article_id = data.substr(num+12,9 );
				var title = $($.parseHTML(data)).find(".product_name");
				title = title.text();
				title = title.split('\n');
				var content = $($.parseHTML(data)).find('#postContent');
				content = content.html();
				content = content.split('<br>');
				var content_s = "";
				for(let j = 0; j<content.length; j++){
					var tmp = $($.parseHTML(content[j])).text();
					if(tmp.length > 0 && tmp!='\n' && tmp != ' '){
						content_s = content_s + "\n" + $.trim(tmp).replace(/\n/gm,"");
					}
				}
				crawling_result.push({number:article_id,title:$.trim(title[2]), price:$.trim(title[3]), content:content_s});
			});
		}
/*
		function crawling(tmp_url){
				return new Promise(function(resolve, reject){
					var jqshr = $.get(src_url+tmp_url, function(data){
						console.log(tmp_url)
						var title = $($.parseHTML(data)).find(".product_name");
						title = title.text();
						title = title.split('\n');
						var content = $($.parseHTML(data)).find('#postContent');
						content = content.html();
						content = content.split('<br>');
						var content_s = "";
						for(let j = 0; j<content.length; j++){
							var tmp = $($.parseHTML(content[j])).text();
							if(tmp.length > 0 && tmp!='\n' && tmp != ' '){
								content_s = content_s + "\n" + $.trim(tmp).replace(/\n/gm,"");
							}
						}
						crawling_result.push({title:$.trim(title[2]), price:$.trim(title[3]), content:content_s});
						resolve();
					});
				});
		}

		async function async_crawling(){
			for(let i=0; i<title_list.length; i++){
				var tmp_url = title_list[i].getAttribute('href')
				var tmp_number = title_number[i].innerText;
				var getresult = await crawling(tmp_url);
			}
			console.log(crawling_result)
		}

		async_crawling();
*/
		for(let i=0; i<numoftitle; i++){
			var tmpvalue = localStorage.getItem(String(article_num[i])+"_changed");
			var before = localStorage.getItem(article_num[i]);
			if(tmpvalue != null){
				was_changed = true;
				title_list[i].innerText = tmpvalue;
				title_list[i].setAttribute('title', before);
			}
		}

		if(was_changed == true && doit == 0){
			chrome.runtime.sendMessage(String(was_changed), response =>{
				console.log(response, " ", doit);
				doit = doit+1;
			});
		}
	}
}

document.addEventListener('changeEvent', function(e) {

	if(document.body.innerHTML.search('main-area') != -1){
		var url = "http://127.0.0.1:8000/server/";

		var data = {'category': categorie, 'keyword': e.data, 'crawlingData': JSON.stringify(crawling_result)};
		console.log(data);
		console.log(crawling_result);

		if( categorie && crawling_result){

			var request_success = false;

			$.ajax({
				url: url,
				dataType: "json",
				data: data,
				type: 'POST',
				success: function(data){

					console.log(data);

					$('.article-board').each(function(index, item){
						if($(item).attr('id') != 'upperArticleList'){
							var children = $(item).find('.td_article');
							children.each(function(index, item){
								var tmp_num = $(item).find('.inner_number').text();
								var tmp_title = localStorage.getItem(String(tmp_num));
								$(item).attr('title', tmp_title);
							});
						}
					});

					console.log(data.length);
					if(data.length <15){
						alert('로그인된 상태로 이용해주세요');
					}

					else{
						for(let i=0; i<numoftitle; ++i){
							var tmp = article_num[i];
							for(let j=0; j<numoftitle; ++j){
								if(data[j].number == tmp){
									var value = data[j].newTitle+"";
									title_list[i].innerText = value;
									localStorage.setItem(String(tmp)+"_changed", value);
								}
							}
						}

						is_changed = true;
						if(is_changed == true){
							chrome.runtime.sendMessage(String(is_changed), response =>{
								is_changed = false;
							});
						}

						request_success = true;

						var junk = document.createElement('script');
						junk.type = 'text/javascript';
						junk.text = ''
						document.head.appendChild(junk);

						chrome.runtime.sendMessage("changeFinished", response=>{
							console.log("changeFinished");
						});
					}
					//this.removeEventListener('changeEvent', arguments.callee);

				},
				error: function(xhr, textStatus, err){
					console.log('readyState: '+xhr.readyState);
					console.log('responseText: '+xhr.responseText);
					console.log('status: '+xhr.status);
					console.log('textStatus: '+textStatus);
					console.log('error: '+err);
					alert("서버 요청에 실패하였습니다.")
				},
				complete: function(){
					if(request_success == false){
						chrome.runtime.sendMessage("FailtoFinish", response=>{
							console.log("FailtoFinish");
						});
					}
				}
			});

		}

	}

});

document.addEventListener('rechangeEvent', function(event){

	for(let i =0; i<numoftitle; i++){
		var tmp = title_number[i].innerText;
		localStorage.removeItem(String(tmp)+"_changed");
		location.reload();
	}

	is_changed = false;
	if(is_changed == false){
		chrome.runtime.sendMessage(String(is_changed), response =>{
			console.log("in rechangeEvent ", response);
			is_changed = true;
		});
	}

	var junk = document.createElement('script');
	junk.type = 'text/javascript';
	junk.text = ''
	document.head.appendChild(junk);
});

chrome.runtime.onMessage.addListener( function(request, sender, sendResponse) {
  var evt = document.createEvent('Event');
  if(request.msg == "change"){
    evt.initEvent('changeEvent', true, false);
		evt.data = request.keyword;
	}
  else if(request.msg == "rechange")
    evt.initEvent("rechangeEvent", true, false);
  document.dispatchEvent(evt);

});

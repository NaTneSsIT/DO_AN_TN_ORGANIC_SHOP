$(document).ready(function(){
	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});

	// Product Variation
	// $(".choose_size2").hide();
	// $(".choose-size").show();
	// const asd = $(".choose-size")
	// console.log(asd)
	// Show size according to selected color
	// $(".choose-color").on('click',function(){
	// 	$(".choose-size").removeClass('active');
	// 	// $(".choose-color").removeClass('focused');
	// 	$(this).addClass('focused');
	//
	// 	// var _color=$(this).attr('data-color');
	// 	//
	// 	// $(".choose-size").hide();
	// 	// $(".color"+_color).show();
	// 	// $(".color"+_color).first().addClass('active');
	//
	// 	var _price=$(".color"+_color).first().attr('data-price');
	// 	$(".product-price").text(_price);
	//
	// });
	// End

	// Show the price according to selected size
	$(".choose_size2").on('click',function(){
		$(".choose-size2").removeClass('active');
		$(this).addClass('active');
		var _index=$(this).attr('data-index');
		console.log('_index')
		var _price=$(this).attr('data-price');
		console.log("price", _price)
		$(".product-price-"+_index).text(_price);
	})

	// End

	// Show the first selected color
	// $(".choose-color").first().addClass('focused');
	// var _color=$(".choose-color").first().attr('data-color');
	// var _price=$(".choose-size").first().attr('data-price');
	//
	// $(".color"+_color).show();
	// $(".color"+_color).first().addClass('active');
	// $(".product-price").text(_price);

	// Add to cart
	$(document).on('click',".add-to-cart",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _qty=$(".product-qty-"+_index).val();
		var _productId=$(".product-id-"+_index).val();
		var _productImage=$(".product-image-"+_index).val();
		var _productTitle=$(".product-title-"+_index).val();
		var _productPrice=$(".product-price-"+_index).text();
		var _productAttribute=$(".product-attribute-"+_index).val();
		console.log(_productAttribute)
		console.log(_productTitle)
		// Ajax
		$.ajax({
			url:'/add-to-cart',
			data:{
				'id':_productId,
				'image':_productImage,
				'qty':_qty,
				'title':_productTitle,
				'price':_productPrice,
				'attribute':_productAttribute,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});
		// End
	});
	// End

	// Delete item from cart
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});
	// $(document).on('click','.delete-all-item',function(){
	// 	var _vm=$(this);
	// 	// Ajax
	// 	$.ajax({
	// 		url:'/delete-all-cart',
	// 		data:{},
	// 		dataType:'json',
	// 		beforeSend:function(){
	// 			_vm.attr('disabled',true);
	// 		},
	// 		success:function(res){
	// 			$(".cart-list").text(res.totalitems);
	// 			_vm.attr('disabled',false);
	// 			$("#cartList").html(res.data);
	// 		}
	// 	});
		// End
	// });
	// Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _maxQTY=$(this).attr('data-qty-max');
		console.log(_maxQTY)
		console.log(_pQty)
		var _vm=$(this);
		// Ajax
		if(parseInt(_maxQTY) >= parseInt(_pQty)){
			$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		}
		else {
			location.reload();
		}

		// End
	});

	// Add wishlist
	$(document).on('click',".add-wishlist",function(){
		var _pid=$(this).attr('data-product');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:"/add-wishlist",
			data:{
				product:_pid
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					_vm.addClass('disabled').removeClass('add-wishlist');
				}
			}
		});
		// EndAjax
	});
	// End

	// Activate selected address
	$(document).on('click','.activate-address',function(){
		var _aId=$(this).attr('data-address');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/activate-address',
			data:{
				'id':_aId,
			},
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					$(".address").removeClass('shadow border-secondary');
					$(".address"+_aId).addClass('shadow border-secondary');

					$(".check").hide();
					$(".actbtn").show();
					
					$(".check"+_aId).show();
					$(".btn"+_aId).hide();
				}
			}
		});
		// End
	});

});
// End Document.Ready

// Product Review Save
$("#addForm").submit(function(e){
	$.ajax({
		data:$(this).serialize(),
		method:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType:'json',
		success:function(res){
			if(res.bool==true){
				$(".ajaxRes").html('Data has been added.');
				$("#reset").trigger('click');
				// Hide Button
				$(".reviewBtn").hide();
				// End

				// create data for review
				var _html='<blockquote class="blockquote text-right">';
				_html+='<small>'+res.data.review_text+'</small>';
				_html+='<footer class="blockquote-footer">'+res.data.user;
				_html+='<cite title="Source Title">';
				for(var i=1; i<=res.data.review_rating; i++){
					_html+='<i class="fa fa-star text-warning"></i>';
				}
				_html+='</cite>';
				_html+='</footer>';
				_html+='</blockquote>';
				_html+='</hr>';

				$(".no-data").hide();

				// Prepend Data
				$(".review-list").prepend(_html);

				// Hide Modal
				$("#productReview").modal('hide');

				// AVg Rating
				$(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
			}
		}
	});
	e.preventDefault();
});
// End
//cancel_order
$(document).on('click','.cancel-order',function(){
		var _pId=$(this).attr('data-order');
		var _vm=$(this);
		console.log(_pId)
		// Ajax
		$.ajax({
			url:'/cancel-order',
			data:{
				'order_id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cancel-order").hide();
				location.reload()
			}
		});
});
$(document).on('click','.statical-1',function(){
		var _start=$('#start_date').val();
		var _end=$('#end_date').val();
		var _vm=$(this);
		console.log(_start)
		console.log(_end)
		// Ajax
		$.ajax({
			url:'/statical1',
			data:{
				'start_date':_start,
				'end_date':_end,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
				window.location.href = "http://127.0.0.1:8000/statical1?start_date="+_start+"&end_date="+_end;
			},
			success:function(res){
			}
		});
});
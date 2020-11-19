
function calculateRow() {
  console.log("in calculate row");
  row = 0;
  var $tblrows = $("#myTable.table.order-list tbody tr");
  $tblrows.each(function (index) {
    var $tblrow = $(this);
    var price = $tblrow.find('input[name^="Cost"]').val();
    var quantity = $tblrow.find('input[name^="Quantity"]').val();
    var rowPriceval = price * quantity;
    console.log(`${row} - ${price} * ${quantity} = ${rowPriceval} `);
    // $(this).find('input[name^="rowPrice"]').text(rowPriceval.toFixed(2));
    $tblrow.find("#rowPrice").val(rowPriceval);
    $("#main_rowPrice").val(rowPriceval);
    // val(rowPriceval.toFixed(2));
  });
}

function calculateGrandTotal() {
  console.log("in call total");
  var grandTotal = 0;
  $("table.order-list").find('[id^=display_dishrowprice]').each(function () {
    console.log($(this).html());  
      grandTotal += parseInt($(this).html());
    });
  console.log("total : " + grandTotal);
  $("#grandtotal").html(grandTotal);
  // document.getElementById()
}


var counter = 0;
$(document).ready(function () {
  // $('#ChangeWaring').alert('close');
  console.log('---------in edit orderDynamic.js !---------');
  let sideid = document.getElementById('SideBarClick');
  // sideid.click();
  // $('#SideBarClick').click();
  $("#ChangeWaring").prop('disabled',true)
  // document.getElementById("ChangeWaring").style.display = 'none';  

  let order_status_div = $('#order_status_div').html();
  $('input[name="Orderstate"][value="'+$.trim(order_status_div)+'"]').prop('checked', true);

  Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
    }); 
  $('#CustOrderDate1').val(new Date().toDateInputValue());
  

  $("table.order-list").on("click", ".ibtnDel", function (event) {
    $(this).closest("tr").remove();
    console.log('______________________________Delete dish________')
    let str = $(this).attr('id');
    let delete_dish_id = str.split('.')[1]
    console.log(delete_dish_id)
    let table = $('#table_name').html();
    let sendData = {
      dish_name: delete_dish_id,
      table_id:table,
      oper:'Delete Dish Row'
    };
    var csrftoken = $.cookie("csrftoken");
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
    
    $.ajax
      ({
        type: "POST",
        url: table+'/AddDish',
        data: sendData,
        success: function (data) {
          console.log("Success");
          calculateGrandTotal();
          document.getElementById("DeletedSuccessful").style.display = 'inherit';
          document.getElementById("UpdateSuccess").style.display = 'none';
          document.getElementById("ChangeWaring").style.display = 'none';
          $("#myTable").load(window.location.href + " #myTable");
          return 1;
        }
      });
    calculateGrandTotal();
    counter -= 1;
  });
});

$('#main_dish').change(function () {
  console.log($('#table_name').html());
  console.log('in select change !');
      var id = $('#main_dish').val();
      var dataString = 'id=' + id;
      //Ajax goes here

      var csrftoken = $.cookie("csrftoken");
      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
      }

      $.ajaxSetup({
        beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });
      let table = $('#table_name').html();
      $.ajax
        ({
          type: "POST",
          url: table+'/SelectPriceGet',
          data: dataString,
          dataType: "json",
          success: function (data) {  
            console.log(data)
            // objx.val(data); //updating cost
            $('#main_cost').val(data);
            return 1;
          }
        });
    });

$('#main_quantity').keyup(function () {
      let q = $('#main_quantity').val()
      let c = $('#main_cost').val()
      $('#main_rowPrice').val(c * q)
      // calculateGrandTotal();
});

//for main add input ------------------Left Side Bottom
$('#add_quantity,#remove_quantity').on("click", function (event) {
  if ($('#main_quantity').val() != '') {
    if ($(this)[0].id == 'add_quantity') {

      let q = $('#main_quantity').val();
      console.log('add', parseInt(q) + 1)
      $('#main_quantity').val(parseInt(q) + 1);
      $('input[name^="Quantity"]').val(parseInt(q) + 1);
      $('#main_quantity').keyup();
    }
    else if ($(this)[0].id == 'remove_quantity') {
      let q = $('#main_quantity').val();
      if ((q - 1) != 0) {
        console.log('remove', parseInt(q) + 1)
        $('#main_quantity').val(parseInt(q) - 1);
        $('input[name^="Quantity"]').val(parseInt(q) - 1);
        $('#main_quantity').keyup();
      }
    }
  }
  // for 
});
//Add Dish button

function DishEntry(frm) {
  console.log("---------------ADD DISH------------------");
  const formData = new FormData(frm);
  let flag = 1;
  let data = ["rishi"];

  for (var value of formData.values()) {
    console.log(value);
    if (value == "") {
      flag = 0;
    }
    data.push(value);
  }

  let dish_name = data[2];
  let dish_quantity = data[4];
  let dish_cost = data[3];
  let table = $('#table_name').html();
  let sendData = {
    dish_name: dish_name,
    dish_quantity: dish_quantity,
    dish_cost:dish_cost,
    table_id:table,
    oper:'AddData'
  };
  console.log(sendData);
  
  $('#main_quantity').val('');
  flag = 1
  if (flag != 0) {
    var csrftoken = $.cookie("csrftoken");
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
    
    $.ajax
      ({
        type: "POST",
        url: table+'/AddDish',
        data: sendData,
        success: function (data) {
          console.log("Success");
          calculateGrandTotal();
          let grandTotal = parseInt($("#grandtotal").html());
          grandTotal+=(parseInt(dish_quantity)*parseInt(dish_cost));
          $("#grandtotal").html(grandTotal);
          $('#main_quantity').val('');
          
          document.getElementById("updateDishQuantity").style.display = 'none';
          document.getElementById("UpdateSuccess").style.display = 'none';
          document.getElementById("ChangeWaring").style.display = 'none';
          document.getElementById("DishAddAlert").style.display = 'inherit';
          // $("#myTable").api().ajax.reload();
          $("#myTable").load(window.location.href + " #myTable");
          // $("#myTable").location.reload(true);
          return 1;
        }
      });
  }
};
//input for + and - for dish
$('[id^=add_quantity] , [id^=remove_quantity]').on("click", function (event) {
  
  let str = $(this)[0].id;
  let operation = str.split('.')[0];
  let dish_id = $.trim(str.split('.')[1].split(' ').join(''));
  let dish_quantity = parseInt($.trim($('#display_quantity_'+dish_id+'').html()));
  let dish_cost = parseInt($.trim($('#display_dishprice_'+dish_id+'').html()));
  let table = $('#table_name').html();
  // let dish_quantity = parseInt(dish_quantity.trim());
  
  if (operation == 'add_quantity')
    dish_quantity+=1
  else
  if (operation == 'remove_quantity')
  {
    if ((dish_quantity) != 0)
      dish_quantity-=1
  }
  
  $('#display_quantity_'+dish_id+'').html(dish_quantity);
  $('#display_dishrowprice_'+dish_id+'').html(dish_quantity*dish_cost);
  document.getElementById("updateDishQuantity").style.display = 'inherit';
  document.getElementById("UpdateSuccess").style.display = 'none';
  document.getElementById("ChangeWaring").style.display = 'inherit';
  document.getElementById("DishAddAlert").style.display = 'none';
  // $('#ChangeWaring').alert();
    calculateGrandTotal()
});

$('#updateDishQuantity').on("click", function (event) {
  //Capturing the Dish Orders table 
  console.log(9)
  let table = $('#table_name').html();
  let data_dishid = [];
  let data_dishPrice = [];
  let data_quantity= [];
  let data_rowPrice= [];
  let $tblrow1 = $('[id^=display_name]')
  $tblrow1.each(function (index) {
    data_dishid.push($(this).html());
  })
  let $tblrow2 = $('[id^=display_dishprice]')
  $tblrow2.each(function (index) {
    let dp = $(this).html();
    data_dishPrice.push(dp.trim());
  })
  let $tblrow3 = $('[id^=display_quantity]')
  $tblrow3.each(function (index) {
    let dq = $(this).html();
    data_quantity.push(dq.trim());
  })
  let $tblrow4 = $('[id^=display_dishrowprice]')
  $tblrow4.each(function (index) {
    let drp = $(this).html()
    data_rowPrice.push(drp.trim());
  })
  console.log(data_dishid)
  console.log(data_dishPrice)
  console.log(data_quantity)
  console.log(data_rowPrice)

  //send to server
  flag = 1
  if (flag==1){
  let sendData = {
    data_dishid: JSON.stringify(data_dishid),
    data_dishPrice: JSON.stringify(data_dishPrice),
    data_quantity: JSON.stringify(data_quantity),
    data_rowPrice: JSON.stringify(data_rowPrice),
    table_id:table,
    oper:'UpdateDataAll'
  };

  var csrftoken = $.cookie("csrftoken");
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
    
    $.ajax({
        type: "POST",
        url: table+'/AddDish',
        data: sendData,
        success: function (data) {
          console.log("Success update in dish");
          document.getElementById("UpdateSuccess").style.display = 'inherit';
          document.getElementById("DeletedSuccessful").style.display = 'none';
          document.getElementById("ChangeWaring").style.display = 'none';
          document.getElementById("DishAddAlert").style.display = 'none';
          // location.reload()
          $("#myTable").load(window.location.href + " #myTable");
          // $("#myTable").location.reload(true);
          // $("#myTable").api().ajax.reload();
          calculateGrandTotal()
          // $("#myTable").load(window.location.href + " #myTable");
          return 1;
        }
      });
    }
  // calculateGrandTotal()
});

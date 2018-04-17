function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(function() {
    $('.datepicker').daterangepicker({ 
    	singleDatePicker: true,
        showDropdowns: true        
    });  

});

$(function() {
	
	$('.ui-pnotify').remove();
	
	$("#reviseFormModalForm").submit(function(e) {

		var form = $("#reviseFormModalForm");
	    var url = form.data('action');
	    $('#reviseFormModal').modal('toggle');
	    appSettings.setItemLoading();	    
	    $.ajax({
	           type: "POST",
	           url: url,
	           data: form.serialize(), // serializes the form's elements.
	           success: function(data)
	           {   	        	   
	        	   $('.loading').hide();
	        	   new PNotify({
                       title: data.title,
                       text: data.message,
                       type: 'info',
                       styling: 'bootstrap3'
                   });
	        	   appRevise.fetchData();	        	   
	           },
	           error: function(XMLHttpRequest, textStatus, errorThrown) {
	        	   $('.loading').hide();
	        	   new PNotify({
                       title: textStatus,
                       text: errorThrown,
                       type: 'error',
                       styling: 'bootstrap3'
                   });	        	   
	           },
	         });  
	    
	    e.preventDefault(); // avoid to execute the actual submit of the form.
	});
	
	
	$("#trackingFormModalForm").submit(function(e) {

		var form = $("#trackingFormModalForm");
	    var url = form.data('action');
	    $('#trackingFormModal').modal('toggle');
	    appSettings.setItemLoading();	    
	    $.ajax({
	           type: "POST",
	           url: url,
	           data: form.serialize(), // serializes the form's elements.
	           success: function(data)
	           {   	        	   
	        	   $('.loading').hide();
	        	   new PNotify({
                       title: data.title,
                       text: data.message,
                       type: 'info',
                       styling: 'bootstrap3'
                   });
	        	   appRevise.fetchData();	        	   
	           },
	           error: function(XMLHttpRequest, textStatus, errorThrown) {
	        	   $('.loading').hide();
	        	   new PNotify({
                       title: textStatus,
                       text: errorThrown,
                       type: 'error',
                       styling: 'bootstrap3'
                   });	        	   
	           },
	         });  
	    
	    e.preventDefault(); // avoid to execute the actual submit of the form.
	});
	
	var appSettings = new Vue({
		el: '#app-settings',
		data: {
			error: '',			
		},
		delimiters: ["<%", "%>"],

		methods: {
			fetchData: function () {
				appRevise.fetchData();
			},			
			setItemLoading: function () {
				 $(this.$el).find('.loading').fadeIn();				 
				 this.error = "";
				 $(this.$el).find('#error-message').fadeOut(); 
			},
			removeItemLoading: function () {
				$(self.$el).find('.loading').hide(); 
			},
			refresh: function () {
				var self = this;
				self.setItemLoading();
				self.fetchData();				
				$(self.$el).find('.loading').hide();
				
			},
		},
	});
	
	var appRevise = new Vue({
		el: '#app-revise',
		data: {
			items: [
			],	
			loading: false,
			error: '',
		},
		delimiters: ["<%", "%>"],
		mounted () {
			console.log("pingRevise");
			this.pingRevise();			
		},
		methods: {			
			checkJob: function (job) {
				var xhr = new XMLHttpRequest()
				var self = this;
				if (!job) {
					this.loading = false;					
					return;
				}
				xhr.open('GET', '/api/jobstatus/' + job + '/');
				xhr.onload = function () {	
					try {
						resp = JSON.parse(xhr.responseText);
				    } catch (e) {
				    	self.error = "Произошла ошибка обновления данных: " + e;
				    }
					
					console.log(resp.job);
					if (resp.job == 'started') {						
						setTimeout(self.checkJob, 1000, job);
					} else {
						self.fetchData();
						self.loading = false;
						NProgress.done();
						if (resp.job == 'failed') {
							self.error = "Произошла ошибка обновления данных";
						}
					} 
				}
				xhr.error = function (e) {
					self.loading = false;
					this.error = "Error " + e.target.status + " occurred while receiving the document.";
				}
				xhr.send();				
			},
			pingData: function (url) {				
				var xhr = new XMLHttpRequest()
				var self = this;
				this.loading = true;				
				xhr.open('GET', url);
				xhr.onload = function () {					
					resp = JSON.parse(xhr.responseText);											
					self.checkJob(resp.job);					 
				}
				xhr.send();
			},
			pingRevise: function () {				
				this.pingData('/api/pingrevise/');				
			},		
			open: function (url) {
				window.location.href = url;
			},			
		}
	});
		
	
	var dateFormat = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/;
	
	function reviver(key, value) {
	    if (typeof value === "string" && dateFormat.test(value)) {
	        return new Date(value);
	    }
	    
	    return value;
	}
	
	var appDealStats = new Vue({
		el: '#app-dealstats',
		data: {
			error: '',
			data: {},
		},
		delimiters: ["<%", "%>"],
		mounted () {
			this.fetchData();			
		},
		filters: {
		  shortdate: function (date) {
			  if (date) {
				  return moment(date).format('DD.MM.YY');
			  }			  
		  },
		  moment: function (date) {
			  if (date) {
				  return moment(date).format('DD.MM.YYYY HH:mm');
			  }
		  }
		},
		methods: {
			fetchData: function () {				
				var xhr = new XMLHttpRequest()
				var self = this;
				xhr.open('GET', '/api/dealstats/');
				xhr.onload = function () {					
					try {
						data = JSON.parse(xhr.responseText, reviver);
						self.data = data.deal_stats; 
						console.log(self.data);
				    } catch (e) {
				    	appSettings.error = "Произошла ошибка обновления данных: " + e;
				    }				
				}
				xhr.send()
			},		
		},
	});
});

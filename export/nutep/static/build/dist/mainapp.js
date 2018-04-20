'use strict';

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

$(function () {
	$('.datepicker').daterangepicker({
		singleDatePicker: true,
		showDropdowns: true
	});
});

$(function () {

	$('.ui-pnotify').remove();

	$("#reviseFormModalForm").submit(function (e) {

		var form = $("#reviseFormModalForm");
		var url = form.data('action');
		$('#reviseFormModal').modal('toggle');
		appSettings.setItemLoading();
		$.ajax({
			type: "POST",
			url: url,
			data: form.serialize(), // serializes the form's elements.
			success: function success(data) {
				$('.loading').hide();
				new PNotify({
					title: data.title,
					text: data.message,
					type: 'info',
					styling: 'bootstrap3'
				});
				appRevise.fetchData();
			},
			error: function error(XMLHttpRequest, textStatus, errorThrown) {
				$('.loading').hide();
				new PNotify({
					title: textStatus,
					text: errorThrown,
					type: 'error',
					styling: 'bootstrap3'
				});
			}
		});

		e.preventDefault(); // avoid to execute the actual submit of the form.
	});

	$("#trackingFormModalForm").submit(function (e) {

		var form = $("#trackingFormModalForm");
		var url = form.data('action');
		$('#trackingFormModal').modal('toggle');
		appSettings.setItemLoading();
		$.ajax({
			type: "POST",
			url: url,
			data: form.serialize(), // serializes the form's elements.
			success: function success(data) {
				$('.loading').hide();
				new PNotify({
					title: data.title,
					text: data.message,
					type: 'info',
					styling: 'bootstrap3'
				});
				appRevise.fetchData();
			},
			error: function error(XMLHttpRequest, textStatus, errorThrown) {
				$('.loading').hide();
				new PNotify({
					title: textStatus,
					text: errorThrown,
					type: 'error',
					styling: 'bootstrap3'
				});
			}
		});

		e.preventDefault(); // avoid to execute the actual submit of the form.
	});

	var appSettings = new Vue({
		el: '#app-settings',
		data: {
			error: ''
		},
		delimiters: ["<%", "%>"],

		methods: {
			fetchData: function fetchData() {
				appRevise.fetchData();
			},
			setItemLoading: function setItemLoading() {
				$(this.$el).find('.loading').fadeIn();
				this.error = "";
				$(this.$el).find('#error-message').fadeOut();
			},
			removeItemLoading: function removeItemLoading() {
				$(self.$el).find('.loading').hide();
			},
			refresh: function refresh() {
				var self = this;
				self.setItemLoading();
				self.fetchData();
				$(self.$el).find('.loading').hide();
			}
		}
	});
});
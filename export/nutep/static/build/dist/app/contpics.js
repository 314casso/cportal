'use strict';

var _utils = require('../utils.js');

var appContpics = new Vue({
    el: '#app-contpics',
    data: {
        items: [],
        loading: false,
        error: '',
        updated: null
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        if (this.$el) {
            this.fetchData();
        }
    },

    methods: {
        checkJob: function checkJob(job) {
            _utils.utils.checkJob(job, this);
        },
        jobSuccess: function jobSuccess() {
            this.fetchData();
        },
        pingService: function pingService() {
            this.loading = true;
            var period = $('#period').data('datepicker').getFormattedDate('ddmmyyyy');
            _utils.utils.pingData('/api/pingcontpics/' + period + '/', this);
        },
        fetchData: function fetchData() {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/contpicsevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    self.items = data;
                    if (self.items) {
                        self.updated = self.items[0].date;
                    }
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function open(url) {
            window.location.href = url;
        },
        log: function log() {
            console.log($('#period').data('datepicker').getFormattedDate('ddmmyyyy'));
        }
    },
    filters: {
        shortdate: function shortdate(date) {
            return _utils.utils.shortdate(date);
        },
        moment: function moment(date) {
            return _utils.utils.moment(date);
        },
        upper: function upper(date) {
            return _utils.utils.upper(date);
        }
    }
});

$('#period').datepicker({
    format: "MM yyyy",
    language: "ru",
    minViewMode: 1,
    maxViewMode: 2
}).on('changeDate', function (e) {
    $(this).datepicker('hide');
});
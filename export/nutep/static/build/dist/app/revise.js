'use strict';

var _utils = require('../utils.js');

var appRevise = new Vue({
    el: '#app-revise',
    data: {
        items: [],
        loading: false,
        error: ''
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        if (this.$el) {
            this.fetchData();
            this.pingRevise();
        }
    },

    methods: {
        checkJob: function checkJob(job) {
            _utils.utils.checkJob(job, this);
        },
        jobSuccess: function jobSuccess() {
            this.fetchData();
        },
        pingRevise: function pingRevise() {
            this.loading = true;
            _utils.utils.pingData('/api/pingrevise/', this);
        },
        fetchData: function fetchData() {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/reviseevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    self.items = data;
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function open(url) {
            window.location.href = url;
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
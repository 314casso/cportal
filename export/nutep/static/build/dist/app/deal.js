'use strict';

var _utils = require('../utils.js');

var appDealStats = new Vue({
    el: '#app-dealstats',
    data: {
        error: '',
        data: {}
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        this.fetchData();
    },

    methods: {
        fetchData: function fetchData() {
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/dealstats/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    self.data = data.deal_stats;
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        }
    },
    filters: {
        shortdate: function shortdate(date) {
            return _utils.utils.shortdate(date);
        },
        moment: function moment(date) {
            return _utils.utils.moment(date);
        }
    }
});
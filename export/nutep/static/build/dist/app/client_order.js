'use strict';

var _utils = require('../utils.js');

Vue.component('v-select', VueSelect.VueSelect);
Vue.component('paginate', VuejsPaginate);

var appTerminalExport = new Vue({
    el: '#app-terminal-export',
    data: {
        items: [],
        orderevents: [],
        loading: false,
        paginate: {
            pageCount: null,
            next: null,
            prev: null,
            page: 1,
            count: 0
        },
        error: '',
        search: '',
        stats: {
            total_rows: 0
        },
        filter: {
            name: '',
            contract: '',
            platform: '',
            perepodacha: '',
            size: [],
            type: [],
            extension: []
        },
        orders: [],
        contract: null,
        selectedOrder: null,
        itemsPerPage: 7
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        this.fetchOrders();
        this.pingOrders();
    },

    computed: {
        isFiltered: function isFiltered() {
            return this.filter.name || this.filter.contract || this.filter.type.length || this.filter.extension.length || this.filter.platform || this.filter.perepodacha;
        },
        filter_name: function filter_name() {
            return this.filter.name;
        },
        filter_contract: function filter_contract() {
            return this.filter.contract;
        },
        filter_platform: function filter_platform() {
            return this.filter.platform;
        },
        filter_perepodacha: function filter_perepodacha() {
            return this.filter.perepodacha;
        },

        filterOptions: function filterOptions() {}
    },
    watch: {
        filter_name: function filter_name(val) {
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();
        },
        filter_contract: function filter_contract(val) {
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();
        },
        filter_platform: function filter_platform(val) {
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();
        },
        filter_perepodacha: function filter_perepodacha(val) {
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();
        }
    },
    methods: {
        formatParams: function formatParams(params) {
            return "?" + Object.keys(params).map(function (key) {
                return key + "=" + encodeURIComponent(params[key]);
            }).join("&");
        },
        selectOrder: function selectOrder(order) {
            this.selectedOrder = order;
        },
        clickCallback: function clickCallback(pageNum) {
            this.paginate.page = pageNum;
            this.fetchOrders();
        },
        customFormatter: function customFormatter(date) {
            return moment(date).format('DD.MM.YYYY');
        },

        checkJob: function checkJob(job) {
            _utils.utils.checkJob(job, this);
        },
        jobSuccessOrders: function jobSuccessOrders() {
            this.fetchOrders();
        },
        jobSuccessOrderData: function jobSuccessOrderData() {},
        pingOrders: function pingOrders() {
            this.loading = true;
            _utils.utils.pingData('/pingorders/', this, this.jobSuccessOrders);
        },
        pingOrderData: function pingOrderData(order) {
            this.loading = true;
            _utils.utils.pingData('/pingorderdata/' + order.id + '/', this, this.jobSuccessOrderData);
        },
        pingContractFiles: function pingContractFiles(contract) {
            this.loading = true;
            _utils.utils.pingData('/pingcontractfiles/' + contract.id + '/', this);
        },
        fetchContractFiles: function fetchContractFiles() {
            var _this = this;

            if (!this.contract) {
                this.items = [];
                this.stats.total_rows = 0;
                this.stats.total_unfiltered = 0;
                return;
            }
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/contractfiles/?contract=' + this.contract.id);
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    _this.items = data;
                } catch (e) {
                    _this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        fetchOrders: function fetchOrders() {
            var _this2 = this;

            NProgress.start();
            var xhr = new XMLHttpRequest();
            var params = {
                page: this.paginate.page
            };
            if (this.isFiltered) {
                params.name = this.filter.name;
                params.contract = this.filter.contract;
                params.platform = this.filter.platform;
                params.perepodacha = this.filter.perepodacha;
            }

            xhr.open('GET', '/api/clientorders/' + this.formatParams(params));
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);

                    var orderevents = data.results;

                    var pageCount = Math.round(data.count / _this2.itemsPerPage);
                    if (pageCount == 0) {
                        pageCount = 1;
                    }

                    _this2.stats.total_rows = data.count;
                    _this2.paginate.count = data.count;
                    _this2.paginate.pageCount = pageCount;
                    _this2.paginate.next = data.next;
                    _this2.paginate.prev = data.prev;
                    var reset = true;
                    NProgress.done();

                    _this2.orderevents = orderevents;

                    if (data.results && data.results.length) {
                        _this2.items = [data.results[0].event];
                        if (!_this2.selectedOrder) {
                            _this2.selectOrder(data.results[0]);
                        }
                    }
                } catch (e) {
                    _this2.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function open(file) {
            var wnd = window.open('about:blank', '_blank');
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/getfileurl/' + file.Guid + '/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText);
                    if (data.url) {
                        wnd.location = data.url;
                    }
                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e + ": " + xhr.responseText;
                }
            };
            xhr.send();
        },
        clearSearch: function clearSearch() {
            this.filter.name = "";
        },
        clearContract: function clearContract() {
            this.filter.contract = "";
        },
        clearPlatform: function clearPlatform() {
            this.filter.platform = "";
        },
        clearPerepodacha: function clearPerepodacha() {
            this.filter.perepodacha = "";
        },
        clearDate: function clearDate() {
            this.filter.date = null;
            console.log('OK');
        },
        clearFilter: function clearFilter() {
            this.filter.name = '';
            this.filter.contract = '';
            this.filter.platform = '';
            this.filter.perepodacha = '';
            this.filter.size = [];
            this.filter.type = [];
            this.filter.extention = [];
        },
        setContainer: function setContainer(terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;
            return true;
        },
        orderlist: function orderlist(item) {
            var rows = this.orderevents.slice();
            return rows;
        },
        rows: function rows(item) {
            if (item && item.contractevent && item.contractevent.files) {
                var rows = item.contractevent.files.slice();

                rows.sort(function (a, b) {
                    if (a.doc_type > b.doc_type) {
                        return 1;
                    }
                    if (a.doc_type < b.doc_type) {
                        return -1;
                    }
                    return 0;
                });

                var self = this;
                var filtered = rows.filter(function (row) {
                    if (!self.isFiltered) {
                        return true;
                    }
                    if (self.filter.name && !(row.title.search(new RegExp(self.filter.name, "i")) != -1)) {
                        return false;
                    }
                    if (self.filter.type.length && !self.filter.type.includes(row.doc_type)) {
                        return false;
                    }
                    if (self.filter.extension.length && !self.filter.extension.includes(row.extension)) {
                        return false;
                    }
                    return true;
                });
                self.stats.total_rows = filtered.length;
                self.stats.total_unfiltered = rows.length;
                return filtered;
            }
        }
    },
    filters: {
        shortdate: function shortdate(date) {
            return _utils.utils.shortdate(date);
        },
        date: function date(_date) {
            return _utils.utils.date(_date);
        },
        moment: function moment(date) {
            return _utils.utils.moment(date);
        },
        upper: function upper(date) {
            return _utils.utils.upper(date);
        },
        number: function number(x) {
            return _utils.utils.number(x);
        },
        humanFileSize: function humanFileSize(size) {
            return _utils.utils.humanFileSize(size);
        }
    }
});
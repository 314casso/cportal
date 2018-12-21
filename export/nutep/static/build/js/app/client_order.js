import {utils} from '../utils.js';

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
            count: 0,
        },
        error: '',
        search: '',        
        stats: {
            total_rows: 0,
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
    mounted() {			        
        this.fetchOrders();
        this.pingOrders();         
    },
    computed: {            
        isFiltered: function () {
            return this.filter.name || this.filter.contract || this.filter.type.length || this.filter.extension.length
            || this.filter.platform || this.filter.perepodacha;
        },
        filter_name() {
            return this.filter.name;
        },
        filter_contract() {
            return this.filter.contract;
        },
        filter_platform() {
            return this.filter.platform;
        },
        filter_perepodacha() {
            return this.filter.perepodacha;
        },
        filterOptions: function () {             
            
        }
    },    
    watch: {
        filter_name: function (val) {            
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();                        
        },
        filter_contract: function (val) {            
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();                        
        },
        filter_platform: function (val) {            
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();                        
        },
        filter_perepodacha: function (val) {            
            this.paginate.page = 1;
            this.selectedOrder = null;
            this.fetchOrders();                        
        },
    },
    methods: {        
        formatParams: function(params){
            return "?" + Object
                  .keys(params)
                  .map(function(key){
                    return key+"="+encodeURIComponent(params[key])
                  })
                  .join("&")
        },
        selectOrder: function(order) {
            this.selectedOrder = order;            
        },
        clickCallback: function(pageNum) {
            this.paginate.page = pageNum;
            this.fetchOrders();
        },
        customFormatter(date) {
            return moment(date).format('DD.MM.YYYY');
        },        
        checkJob: function (job) {
            utils.checkJob(job, this);
        },
        jobSuccessOrders: function () {            
            this.fetchOrders();             
        },
        jobSuccessOrderData: function () {            
            
        },
        pingOrders: function () {
            this.loading = true;
            utils.pingData('/pingorders/', this, this.jobSuccessOrders);
        },
        pingOrderData: function (order) {
            this.loading = true;
            utils.pingData('/pingorderdata/' + order.id + '/',this, this.jobSuccessOrderData);
        },
        pingContractFiles: function (contract) {
            this.loading = true;
            utils.pingData('/pingcontractfiles/' + contract.id + '/', this);
        },
        fetchContractFiles: function () {            
            if (!this.contract) {
                this.items = []
                this.stats.total_rows = 0;
                this.stats.total_unfiltered = 0;    
                return;
            }
            var xhr = new XMLHttpRequest();            
            xhr.open('GET', '/api/contractfiles/?contract=' + this.contract.id);
            xhr.onload = () => {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    this.items = data;	                    
                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },        
        fetchOrders: function () {            
            NProgress.start();
            var xhr = new XMLHttpRequest();            
            var params = {
                page: this.paginate.page,                 
            };
            if (this.isFiltered) {
                params.name = this.filter.name;
                params.contract = this.filter.contract;
                params.platform = this.filter.platform;
                params.perepodacha = this.filter.perepodacha;
            }
            
            xhr.open('GET', '/api/clientorders/' + this.formatParams(params));
            xhr.onload = () => {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                                        
                    let orderevents = data.results;   

                    let pageCount = Math.round(data.count / this.itemsPerPage);
                    if (pageCount == 0) {
                        pageCount = 1;
                    }
                    
                    this.stats.total_rows = data.count;
                    this.paginate.count = data.count;
                    this.paginate.pageCount = pageCount;
                    this.paginate.next = data.next;
                    this.paginate.prev = data.prev;
                    var reset = true;
                    NProgress.done();
                 

                    this.orderevents = orderevents;

                    if (data.results && data.results.length) {
                        this.items =  [data.results[0].event];
                        if (!this.selectedOrder) {
                            this.selectOrder(data.results[0]);                     
                        }
                    }

                } catch (e) {
                    this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function (file) {
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
                }
                xhr.send();
        },        
        clearSearch: function () {
            this.filter.name = "";
        },
        clearContract: function () {
            this.filter.contract = "";
        },
        clearPlatform: function () {
            this.filter.platform = "";
        },
        clearPerepodacha: function () {
            this.filter.perepodacha = "";
        },
        clearDate: function () {
            this.filter.date = null;            
            console.log('OK');
        },
        clearFilter: function () {
            this.filter.name = '';
            this.filter.contract = '';
            this.filter.platform = '';
            this.filter.perepodacha = '';
            this.filter.size = [];
            this.filter.type = [];
            this.filter.extention = [];                        
        },        
        setContainer: function (terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;                        
            return true;
        }, 
        orderlist: function (item) {            
            let rows = this.orderevents.slice();
            return rows;
        },               
        rows: function (item) {
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
        },
    },
    filters: {
        shortdate: (date) => {
            return utils.shortdate(date);
        },
        date: (date) => {
            return utils.date(date);
        },
        moment: (date) => {				
            return utils.moment(date);									
        },
        upper: (date) => {
            return utils.upper(date);					
        },
        number: (x) => {
            return utils.number(x);					
        },
        humanFileSize: (size) => {            
            return utils.humanFileSize(size);
        },
    },
});


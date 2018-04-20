export {utils}

const utils = {		    
    reviver: function reviver(key, value) {
        const dateFormat = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/;
        if (typeof value === "string" && dateFormat.test(value)) {
            return new Date(value);
        }    
        return value;
    },
    checkJob: function (job, app) {					
        app.loading = true;			
        var xhr = new XMLHttpRequest();			
        if (!job) {									
            app.loading = false;
            return;
        }
        xhr.open('GET', '/api/jobstatus/' + job + '/');
        xhr.onload = function () {
            try {
                var resp = JSON.parse(xhr.responseText);
            } catch (e) {
                app.error = "Произошла ошибка обновления данных: " + e;
            }								
            if (resp.job == 'started') {					
                setTimeout(utils.checkJob, 1000, job, app);
            } else {					
                app.loading = false;					
                if (resp.job == 'failed') {
                    app.error = "Произошла ошибка обновления данных";
                } else {
                    app.jobSuccess();
                }
            }
        };
        xhr.error = function (e) {
            app.loading = false;
            app.error = "Error " + e.target.status + " occurred while receiving the document.";
        };
        xhr.send();
    },
    pingData: function (url, app) {
        var xhr = new XMLHttpRequest();			
        app.loading = true;
        xhr.open('GET', url);
        xhr.onload = function () {
            var resp = JSON.parse(xhr.responseText);
            utils.checkJob(resp.job, app);
        };
        xhr.send();
    },
    
    shortdate: function (date) {
        if (date) {
            return moment(date).format('DD.MM.YY');
        }
    },    
    moment: function (date) {
        if (date) {
            return moment(date).format('DD.MM.YYYY HH:mm');
        }
    },
    upper: function (date) {
        if (date) {
            return date.toUpperCase();
        }
    },
    number: function(x) {
        if (!x) {
            return null;
        }
        return parseFloat(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, String.fromCharCode(160));
    },
    sum: function(items, prop){
        return items.reduce( function(a, b){
            return a + parseFloat(b[prop]);
        }, 0);
    }
  };
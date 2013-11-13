function PyCached(host) {
    this.host = host;
};

/**
 * Call pycached synchronously and return the value.
 */
PyCached.prototype.run = function run(request) {
    var res;
    $.ajax({
      url: this.host,
      type: "POST",
      async: false,
      data: request
    }).done(function(data, textStatus, jqXHR){
      res = data;
    });
    return res;
};

PyCached.prototype.version = function version() {
    return this.run({command:'version'});
};

PyCached.prototype.count = function count() {
    return parseInt(this.run({command:'count'}), 10);
};

PyCached.prototype.clear = function clear() {
    return this.run({command:'clear'});
};

PyCached.prototype.items = function items() {
    return this.run({command:'items'});
};

PyCached.prototype.status = function status() {
    return this.run({command:'status'});
};

PyCached.prototype.get = function get(key) {
    return this.run({command:'get', key: key});
};

PyCached.prototype.set = function set(key, value) {
    return this.run({command:'set', key: key, value: value});
};

PyCached.prototype.delete = function _delete(key) {
    return this.run({command:'delete', key: key});
};

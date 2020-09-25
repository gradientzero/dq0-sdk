/*!
 * DQ0 SDK Javascript version
 *
 * Copyright 2020, Gradient Zero
 * All rights reserved
 */

(function (window, undefined) {
    
    var XHR = (function() {
      var that = {
        send: function(url, payload, successCallback, failureCallback) {
          var body = JSON.stringify(payload);
          
          var xhr = new XMLHttpRequest();
          if (successCallback) {
            xhr.onload = function() {
               successCallback(xhr.response);
            };
          }
    
          if (failureCallback) {
            xhr.onerror = function() {
              failureCallback(xhr.response);
            };
          }
    
          xhr.open('POST', url);
          xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
          xhr.send(body);
        }
      };
      return that;
    })();
    
    var endpoint       = 'https://sdk.dq0.io/api/v1/events/';
    var name           = 'dq0.sdk.js';
    var version        = '0.0.1';
    var appID          = null;
    
    var getNewAppID = function() {
      var id = '';
      for (var i=0; i < 20; i++) {
        id += Math.floor(16*Math.random()).toString(16);
      }
      return id;
    };
    
    var DQ0 = {
      /** Sets the app ID. */
      setAppID: function(newAppID) {
        appID = newAppID;
      },
      
      /** Send a tracking event.
        *
        * Example:
        * DQ0.send('some_event', { 'some_param': 'some-value' });
        */
      send: function(event, params, successCallback, failureCallback) {
        appID = appID || getNewAppID()
        params = params || {}
        payload = {}
        payload['event'] = event
        payload['appID'] = appID
        payload['sdk'] = name
        payload['version'] = version
        payload['params'] = JSON.stringify(params)
        XHR.send(endpoint, payload, successCallback, failureCallback);
      },
      
      
      /** App started event. */
      appStarted: function(newAppID, params, successCallback, failureCallback) {
        appID = newAppID || appID;
        this.send('app_start', params, successCallback, failureCallback);
      }
    };
    
    window.DQ0 = DQ0;
})(window);
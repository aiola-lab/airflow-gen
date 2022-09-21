/**
 * Jupyter Notebooks Extensions
 *
 **/
 define([
  'require',
  'jquery',
  'base/js/namespace',
  'base/js/events',
  "base/js/dialog"
], function (
  require,
  $,
  IPython,
  events,
  dialog
) {
  // 'use strict';

  var config_added = false;
  var config_hidden = false;
  function generate_dag_from_notebook() {
      IPython.keyboard_manager.disable();
      var button = $('<button/>').addClass('btn-primary').text('Generate').on('click', function () {
              function callback(out){
                console.log("OUT: "+ JSON.stringify(out));
              }
              var callbacks = { iopub: { output: callback } };
              var config = {
                "email": $("#email").val(),
                "owner": $("#owner").val(),
                "retries": $("#retries").val(),
                "use_all": $("#use_all").val(),
                "s3_sensor_path": $("#s3_sensor_path").val(),
                "retry_delay": "timedelta(days=1)",
                "start_date": "datetime(2022, 1, 1)",
                "interval": "@hourly",
                "flow": $("#flow").val(),
              }
              config_str = JSON.stringify(config).replace('"', '\"');
              cmd = `%run src/generator.py '${config_str}'`
              console.log("Command: "+ cmd)
              IPython.notebook.kernel.execute(cmd,callbacks,
                              { silent: false })
              return true;
      })
      if(!config_added){
        show_config_form(button);
        config_added = true;
      }
      // if (config_hidden){
      //   $('#config').show();
      // }else{
      //   $('#config').hide();
      //   config_hidden = true;
      // }
  } // function generate_dag_from_notebook

  var load_ipython_extension = function () {
    if (!IPython.toolbar) {
      $([IPython.events]).on(
        "app_initialized.NotebookApp",
        add_toolbar_buttons
      );
      return;
    } else {
      add_toolbar_buttons();
    }
  };
  var show_config_form = function(button){
      var body = $("<p align=center border='1' >");
      body.append('<div id="side_panel">');
      body.append($("<h4/>").text("Do you want to generate DAG from this notebook?"))
      body.append(
        $(" \
            <form id='config' >\
            <label for='email'>Email:</label>\
            <input type='email' id='email' name='email'/>\
            <label for='owner'>Owner:</label>\
            <input type='text' id='owner' name='owner'/> <br/>\
            <label for='retries'>Retries (between 1 and 5):</label>\
            <input type='number' id='retries' name='retries' min='1' max='5'>\
            <label for='retry_delay'>Retries Delay:</label>\
            <input type='number' id='retry_delay_num' name='retries' min='1' max='5'>\
            <select type='number' id='retry_delay' name='retry_delay' min='1' max='5'>\
              <option value='day'>days</option>\
              <option value='hour'>houts</option>\
              <option value='minute'>minutes</option>\
            </select>\
            </br>\
            <label for='s3_sensor_path'>S3 Sensor path (Optional)</label>\
            <input type='text' id='s3_sensor_path' name='s3_sensor_path'/>\
            <label for='use_all'>Use all notebooks for DAG?</label>\
            <input type='checkbox' id='use_all' name='use_all' checked/><br/>\
            </form> </div>\
          ")
      ).append(button)
      body.insertBefore($('#notebook_panel'))
  }
  var add_toolbar_buttons = function () {
    Jupyter.actions.register(
      {
        help: "Generate DAG from notebook",
        icon: "fa-cog",
        handler: generate_dag_from_notebook,
      },
      "generate_dag_from_notebook",
      "generate"
    );

    IPython.toolbar.add_buttons_group(
      [
        {
          action: "generate:generate_dag_from_notebook",
        },
      ],
      "generate-buttons"
    );
  };

  return {
    load_ipython_extension: load_ipython_extension,
  };
});

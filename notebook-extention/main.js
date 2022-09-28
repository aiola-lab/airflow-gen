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
                if(out)
                alert('Generated DAG under `generated` directory');
                console.log("OUT: "+ JSON.stringify(out));
              }
              var callbacks = { iopub: { output: callback } };
              var config = {
                "email": $("#email").val(),
                "owner": $("#owner").val(),
                "retries": $("#retries").val(),
                "s3_sensor_path": $("#s3_sensor_path").val(),
                "retry_delay": "timedelta("+$("#retry_delay").val()+"="+$("#retry_delay_num").val()+")",
                "start_date": "datetime(2022, 1, 1)",
                "interval": $("#schedule_interval").val(),
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
      }else if(config_hidden){
        $("#side_panel").show();
        config_hidden=false;
      }else{
        $("#side_panel").hide();
        config_hidden=true;
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
      var body = $("<div style='width:800px; margin:0 auto;' id='side_panel' name='side_panel'>");
      body.append($("<h4/>").text("Do you want to generate DAG from this notebook?"))
      body.append(
        $(" \
            <form id='config' >\
            <!--label for='email'>Email:</label-->\
            <input type='hidden' id='email' value='dag@aiola.com' name='email'/>\
            <!--label for='owner'>Owner:</label-->\
            <input type='hidden' id='owner' value='aiola_dag_generator' name='owner'/> <br/>\
            <label for='schedule_interval'>DAG Schedule interval:</label>\
            <input type='text' id='schedule_interval' value='@daily'/></br>\
            <label for='retries'>Retries (between 1 and 5):</label>\
            <input type='number' id='retries' value=2 required name='retries' min='1' max='5'></br>\
            <label for='retry_delay'>Retries Delay:</label>\
            <input type='number' id='retry_delay_num' value='1' name='retries' min='1' max='5'>\
            <select id='retry_delay' value='minute' name='retry_delay'>\
              <option value='minute'>minutes</option>\
              <option value='hour'>hours</option>\
              <option value='day'>days</option>\
            </select>\
            </br>\
            <!--label for='s3_sensor_path'>S3 Sensor path (Optional)</label-->\
            <input type='hidden' id='s3_sensor_path' name='s3_sensor_path'/>\
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

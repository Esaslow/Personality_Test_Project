//console.log('GET FUCKED AND DIE');
// This is a comment
//$ is jquery
var model_number = 0
var model_string = 'model'+model_number.toString();

$(document).ready(function(){
  console.log('webpage is ready');
  $('#model0').hide()
  $('#model1').hide()
  $('#model2').hide()
  $('#model3').hide()
  $('#model4').hide()
  $('.GetNextQuestion').hide()
  $('#Graph1').hide()
  $('#Graph2').hide()
  $('.slider_text').hide()
  $('.NumberModelsRemaining').hide()
  $('.Button_Tab').hide()
  //$ Looks for a tage on a page
  //async makes it asyncrnous
  $('#Startquiz').click(async function(){
    console.log('Button was clicked');
    const response = await $.ajax('/Startquiz',{})
    console.log('response',response)
    $('#model0').show()
    $('.slider_text').show()
    $('.NumberModelsRemaining').show()
    $('#Startquiz').hide()
    $('#intro').hide()
    $('.GetNextQuestion').show()
    $('.Button_Tab').show()
    $('.slider_val').text((25).toString())
    $('.NumberModelsRemaining').text('Traits Remaining = '+(5-model_number).toString() )
    $('#model0 .Question').text(response.question)
    model_number = response.model_number
    console.log(model_number)

    $('#'+model_string+' .slider')[0].oninput = function(){
      $('.slider_val').text(this.value)
    }
  })

  $(' .GetNextQuestion').click(async function(){
    $('#'+model_string+' .slider')[0].oninput = function(){
      $('.slider_val').text(this.value)
      }
    // Clicked the button get next question
    console.log('Button was clicked');

    var butt = $('#'+model_string+' .slider')[0].value
    $('#'+model_string+' .slider')[0].value = '25'
    $('.slider_val').text(25)
    // *** NEED IMPROVEMENT ***
    //Get the variable from the slider





    //print out the value from the slider in the consol
    console.log(butt)
    const user_resp = butt;


    //create a dictionary that holds the dat
    const data = {
      user_resp,
      model_number

    }
    //print out the data
    console.log(data)
    // Send the data to the server and get the response back

    const next_question = await $.ajax('/GetNextQuestion',{
      data: JSON.stringify(data),
      method: "post",
      contentType: "application/json"
    })
    //Check to see if the flag is there.  Not sure that
    //I use this. I used the implmintation of includes
    // instead
    console.log(next_question.flag)
    const flag = next_question.flag

    //If we get to the end of a node:
    if (next_question.question.includes('you')){
      console.log(model_number)
      if (model_number == 4){
        const df = await $.ajax('/reccomend');
        $('.GetNextQuestion').hide()
        $('#Graph1').show()
        $('#Button_Tab').hide()
        //$('#scatter-button').click(async function(){
        console.log('scatter')
        const d = await $.ajax('/plot');
        const size = d.size
        const text1 = d.text
        console.log(text1)
        const trace = [{
          x:[-5,-5,0,5,5],
          y:[-5,5,0,-5,5],
          mode:'markers+text',
          marker:{
            color:['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(146, 56, 153)','rgb(255, 65, 54)'],
            size:size,
            },
          text:text1,
          textposition:'top'
          }];
        const layout = {
                xaxis:{
                  range:[-8,7],
                  showgrid:false,
                  zeroline:false,
                  showline:false,
                  autotick:true,
                  ticks:'',
                  showticklabels:false
                },
                yaxis:{
                  range:[-8,10],
                  showgrid:false,
                  zeroline:false,
                  showline:false,
                  autotick:true,
                  ticks:'',
                  showticklabels:false
                },
                width:700,
                height:600,
                hovermode: 'closest',
                title: 'The results from your personality test'
                        }

        Plotly.plot($('#Graph1')[0],trace,layout);
        const t = await $.ajax('/reccomend');
        $('#Graph2').show()

        const barg = [t[0].trace0, t[0].trace1, t[0].trace2, t[0].trace3, t[0].trace4];
        const layout2 = {
                width:700,
                height:600,
                hovermode: 'closest',
                title: 'The Facets from your personality test'
                        }
        Plotly.plot($('#Graph2')[0], {data: barg,layout:layout2});
        //Plotly.plot($('#Graph2')[0],trace2[0].trace0);

                          }
      //print out the end of tree string
      $('#'+model_string+' .Question').text(next_question.question)
      $('#'+model_string+' .slidecontainer').hide()
      //Update the Model Number & string
      model_number = Number(model_number) + 1
      $('.NumberModelsRemaining').text('Traits Remaining = '+(5-model_number).toString() )
      model_string = 'model'+model_number.toString();

      // Print out the model string so that we know
      // we are at the right spot
      console.log(model_string)

      //Show the next part div tag
      $('#'+model_string).show()


      // Send the data to the server and get the response back
      const upcoming = await $.ajax('/nextQuiz',
      {
        // send the model number to the server
        data: JSON.stringify({model_number: model_number}),
        method: "post",
        contentType: "application/json"
      })

      //Print out the upcoming question in console
      console.log(upcoming.question)

      // set the next div tag to the string
      $('#'+model_string+' .slider')[0].oninput = function(){
        $('.slider_val').text(this.value)
      }
      $('#'+model_string+' .Question').text(upcoming.question)}

    // Otherwise just update the tag to the next question
    else {
      $('#'+model_string+' .Question').text(next_question.question)
          }

  });


});

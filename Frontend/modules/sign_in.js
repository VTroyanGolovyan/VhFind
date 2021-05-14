let signinModule = new Module({
  template: './templates/sign_in.html',
  model: {
    email: '',
    password: ''
  },
  handlers: {
    loginButton: function(model) {
      VHrequest({
        method: 'POST',
        url: SERVER + '/sign/in',
        data: {
          email: model.email,
          password: model.password
        }
      }).then((response) => {
        try {
          data = JSON.parse(response)
          alert(data.data)
          if (data.data == '') {
            return
          }
          window.localStorage.setItem('token', data.data)
          document.location.hash = '#/'
        } catch (e) {

        } finally {

        }

      })
    }
  }
})

document.addEventListener('DOMContentLoaded', function () {


  const alertWrappers = document.querySelectorAll('.alert');

  alertWrappers.forEach(alertWrapper => {
    const closeBtn = alertWrapper.querySelector('.alert__close');


    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        alertWrapper.remove();
      });
    }
  });
});

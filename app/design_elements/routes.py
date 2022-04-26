from flask import redirect, render_template, Blueprint, request, current_app, Response, send_file, url_for

from app.design_guides.models import Designguide
from .models import Designelement, Logo, Font, Color, Keyword
from werkzeug.utils import secure_filename
from app.extensions.database import db
from flask_login import current_user, login_required, login_user
blueprint = Blueprint('elements' , __name__)


@blueprint.route('/elements')
@login_required
def design_elements():
  page_number = request.args.get('page', 1, type=int)
  elements_pagination = Designelement.query.paginate(page_number, current_app.config['ELEMENTS_PER_PAGE'])

  return render_template('design_elements/index.html', elements_pagination=elements_pagination)

@blueprint.route('/elements/<slug>')
@login_required
def element(slug):
  element = Designelement.query.filter_by(slug=slug).first_or_404()
  return render_template('design_elements/show.html', element=element)



@blueprint.post('/elements/logo/upload')

def upload_logo():
  try:
    logo = request.files['Logo']

    if not logo:
      raise Exception( 'Something went Wrong :/')

    filename = secure_filename(logo.filename)
    mimetype = logo.mimetype
    buffer = Logo(buffer = logo.read(), mimetype = mimetype, name = filename, designguide_id = current_user.id)
    buffer.save()
    db.session.add(buffer)
    db.session.commit()
    element = 'Logo'
    success = f'Your {element} have been successfully uploaded'
    return render_template('design_elements/show.html', element= element, success = success)

  except Exception as error_message:
    element = 'Logo'
    error = error_message or 'An error occurred while processing your Upload. Please avoid uploading the same logo more than once.'
    return render_template('design_elements/show.html', element= element, error= error)

@blueprint.post('/elements/font/upload')
def upload_font():
  font = request.files['Font']

  if not font:
    return 'Something went Wrong :/', 400

  filename = secure_filename(font.filename)
  mimetype = font.mimetype
  buffer = Font(buffer = font.read(), mimetype = mimetype, name = filename, designguide_id = current_user.id)
  db.session.add(buffer)
  
  
  db.session.commit()
  element = 'Font'
  success = f'Your {element} have been successfully uploaded'
  return render_template('design_elements/show.html', element= element, success = success)






@blueprint.post('/elements/color/upload')

def upload_color():
  try:
    color1 = request.form.get('color1')
    color2 = request.form.get('color2')
    color3 = request.form.get('color3')
    color4 = request.form.get('color4')
    color5 = request.form.get('color5')
    color6 = request.form.get('color6')  
    
    if not color1 and color2 and color3:
      error = 'Please upload at least 3 colors'
      return render_template('design_elements/show.html', error = error)

    color_palette = Color(
    color1 = request.form.get('color1'),
    color2 = color2,
    color3 = color3,
    color4 = color4,
    color5 = color5,
    color6 = color6,
    designguide_id = current_user.id
    )
    
    color_palette.save()

    db.session.add(color_palette)
    

    db.session.commit()

    element = 'Color Palette'
    success = f'Your {element} have been successfully uploaded'
    return render_template('design_elements/show.html', element= element, success = success)
  except Exception as error_message:
    error = error_message or 'An error occurred while processing your Upload.'
    return redirect(url_for('elements.element', slug='color', error= error))


@blueprint.post('/elements/keywords/upload')

def upload_keywords():
  try:
    keyword1 = request.form.get('keyword1')
    keyword2 = request.form.get('keyword2')
    keyword3 = request.form.get('keyword3')
    keyword4 = request.form.get('keyword4')
    keyword5 = request.form.get('keyword5')
    keyword6 = request.form.get('keyword6')  

    if not keyword1 and keyword2 and keyword3:
      raise Exception('Please upload at least 3 keywords')


    keywords = Keyword(
    keyword1 = keyword1,
    keyword2 = keyword2,
    keyword3 = keyword3,
    keyword4 = keyword4,
    keyword5 = keyword5,
    keyword6 = keyword6,
    designguide_id = current_user.id
  )

    keywords.save()
    db.session.add(keywords)
    
   
    db.session.commit()

    element = 'Keywords'
    success = f'Your {element} have been successfully uploaded'
    return render_template('design_elements/show.html', element= element, success = success)
  except Exception as error_message:
    error = error_message or 'An error occurred while processing your Design Guide. Please make sure to enter valid data.'
    return redirect(url_for('elements.element', slug='keywords', error= error))
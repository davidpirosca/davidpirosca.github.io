from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import re

class GestionPracticasProfesor(models.Model):
    _name = "gestionpracticas.profesor"
    _description = 'Modelo para Profesores'

    dni = fields.Char(string="DNI", required=True)
    name = fields.Char(string="Nombre y Apellidos", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    direccion = fields.Char(string="Dirección", required=True)
    telefono = fields.Char(string="Teléfono", required=True)
    email = fields.Char(string="Correo Electrónico", required=True)
    id_ciclo_formativo = fields.Many2one('gestionpracticas.ciclos_formativos', string='Ciclo Formativo', required=True)
    id_alumnos = fields.One2many('gestionpracticas.alumno', 'profesor', string='Alumnos')
    foto = fields.Binary(string="Foto")
    total_alumnos = fields.Integer(string="Total de Alumnos", compute="_compute_total_alumnos", store=True)

    @api.model
    def send_welcome_email(self):
        template = self.env.ref("gestionpracticas.email_template_welcome_profesor")
        template.send_mail(self.id, force_send=True)
    
    @api.depends('id_alumnos')
    def _compute_total_alumnos(self):
        for profesor in self:
            profesor.total_alumnos = len(profesor.id_alumnos)

    @api.constrains('dni')
    def _check_dni_format(self):
        for record in self:
            if record.dni and not re.match("^[0-9]{8,9}[A-Za-z]$", record.dni):
                raise ValidationError("El DNI debe contener 8 o 9 números seguidos por una letra.")

    @api.constrains('name')
    def _check_name_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if not record.name:
                raise ValidationError("El nombre y apellidos no puede estar vacío.")
            
            # Verificar que el nombre solo contiene letras y espacios
            if not all(char.isalpha() or char.isspace() for char in record.name):
                raise ValidationError("El nombre y apellidos solo debe contener letras y espacios.")

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            # Verificar que la fecha de nacimiento no sea en el futuro
            if record.fecha_nacimiento and record.fecha_nacimiento > date.today():
                raise ValidationError("La fecha de nacimiento no puede estar en el futuro.")
            
            # Verificar que la persona tenga más de 18 años
            edad_minima = timedelta(days=365 * 18)  # 18 años en días aproximados
            if record.fecha_nacimiento and record.fecha_nacimiento > (datetime.now().date() - edad_minima):
                raise ValidationError("La persona debe tener al menos 18 años.")
    
    @api.constrains('telefono')
    def _check_telefono_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if record.telefono and not record.telefono.isdigit():
                raise ValidationError("El teléfono debe contener solo números.")

            # Verificar la longitud del teléfono
            if record.telefono and (len(record.telefono) < 9 or len(record.telefono) > 12):
                raise ValidationError("La longitud del teléfono debe estar entre 9 y 12 caracteres.")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if record.email:
                # Verificar el formato del correo electrónico
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("El formato del correo electrónico no es válido.")

    _sql_constraints = [
        ('unique_dni_profesor', 'UNIQUE(dni)', 'El DNI del profesor debe ser único.'),
         ('check_dni_length', 'CHECK(length(dni) = 9)', 'El DNI debe tener 9 caracteres.'),
    ]

class GestionPracticasCiclosFormativos(models.Model):
    _name = "gestionpracticas.ciclos_formativos"
    _description = 'Modelo para Ciclos Formativos'

    name = fields.Char(string="Nombre del Ciclo", help="Introduce el nombre del Ciclo Formativo", required=True)
    coordinador = fields.Many2one('gestionpracticas.profesor', string='Coordinador del Ciclo')
    profesores = fields.Many2many('gestionpracticas.profesor', string='Profesores del Ciclo', relation='ciclo_profesor_rel')

    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name) <= 3:
                raise ValidationError("El nombre del ciclo formativo debe tener más de 3 caracteres.")

    _sql_constraints = [
        ('unique_name_ciclo_formativo', 'UNIQUE(name)', 'El nombre del ciclo formativo debe ser único.')
    ]

class GestionPracticasAlumno(models.Model):
    _name = "gestionpracticas.alumno"
    _description = 'Modelo para Alumnos'

    dni = fields.Char(string="DNI", required=True)
    name = fields.Char(string="Nombre y Apellidos", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    direccion = fields.Char(string="Dirección")
    telefono = fields.Char(string="Teléfono", required=True)
    email = fields.Char(string="Correo Electrónico", required=True)
    id_ciclo_formativo = fields.Many2one('gestionpracticas.ciclos_formativos', string='Ciclo Formativo', required=True)
    profesor = fields.Many2one('gestionpracticas.profesor', string='Profesor')
    foto = fields.Binary(string="Foto")

    @api.constrains('dni')
    def _check_dni_format(self):
        for record in self:
            if record.dni and not re.match("^[0-9]{8,9}[A-Za-z]$", record.dni):
                raise ValidationError("El DNI debe contener 8 o 9 números seguidos por una letra.")

    @api.constrains('name')
    def _check_name_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if not record.name:
                raise ValidationError("El nombre y apellidos no puede estar vacío.")
            
            # Verificar que el nombre solo contiene letras y espacios
            if not all(char.isalpha() or char.isspace() for char in record.name):
                raise ValidationError("El nombre y apellidos solo debe contener letras y espacios.")

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            # Verificar que la fecha de nacimiento no sea en el futuro
            if record.fecha_nacimiento and record.fecha_nacimiento > date.today():
                raise ValidationError("La fecha de nacimiento no puede estar en el futuro.")
            
            # Verificar que la persona tenga más de 16 años
            edad_minima = timedelta(days=365 * 16)  # 16 años en días aproximados
            if record.fecha_nacimiento and record.fecha_nacimiento > (datetime.now().date() - edad_minima):
                raise ValidationError("La persona debe tener al menos 16 años.")
    
    @api.constrains('telefono')
    def _check_telefono_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if record.telefono and not record.telefono.isdigit():
                raise ValidationError("El teléfono debe contener solo números.")

            # Verificar la longitud del teléfono
            if record.telefono and (len(record.telefono) < 9 or len(record.telefono) > 12):
                raise ValidationError("La longitud del teléfono debe estar entre 9 y 12 caracteres.")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if record.email:
                # Verificar el formato del correo electrónico
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("El formato del correo electrónico no es válido.")

    _sql_constraints = [
        ('unique_dni_alumno', 'UNIQUE(dni)', 'El DNI del alumno debe ser único.'),
         ('check_dni_length', 'CHECK(length(dni) = 9)', 'El DNI debe tener 9 caracteres.'),
    ]

class GestionPracticasEmpresa(models.Model):
    _name = "gestionpracticas.empresa"
    _description = 'Modelo para Empresas'

    name = fields.Char(string="Nombre de la Empresa", required=True)
    direccion = fields.Char(string="Dirección", required=True)
    email = fields.Char(string="Correo Electrónico")
    telefono = fields.Char(string="Teléfono", required=True)
    responsable = fields.Char(string="Responsable", required=True)

    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name) <= 3:
                raise ValidationError("El nombre de la empresa debe tener más de 3 caracteres.")

    @api.constrains('telefono')
    def _check_telefono_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if record.telefono and not record.telefono.isdigit():
                raise ValidationError("El teléfono debe contener solo números.")

            # Verificar la longitud del teléfono
            if record.telefono and (len(record.telefono) < 9 or len(record.telefono) > 12):
                raise ValidationError("La longitud del teléfono debe estar entre 9 y 12 caracteres.")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if record.email:
                # Verificar el formato del correo electrónico
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("El formato del correo electrónico no es válido.")

    @api.constrains('responsable')
    def _check_name_format(self):
        for record in self:
            # Verificar que el campo no esté vacío
            if not record.name:
                raise ValidationError("El Responsable no puede estar vacío.")
            
            # Verificar que el nombre solo contiene letras y espacios
            if not all(char.isalpha() or char.isspace() for char in record.name):
                raise ValidationError("El Repsonsable solo debe contener letras y espacios.")

    _sql_constraints = [
        ('unique_name_empresa', 'UNIQUE(name)', 'El nombre de la empresa debe ser único.')
    ]

class GestionPracticasPractica(models.Model):
    _name = "gestionpracticas.practica"
    _description = 'Modelo para Prácticas Estudiantiles'

    name = fields.Many2one('gestionpracticas.alumno', string='Alumno', required=True)
    id_profesor = fields.Many2one('gestionpracticas.profesor', string='Profesor', required=True)
    id_ciclo = fields.Many2one('gestionpracticas.ciclos_formativos', string='Ciclo Formativo')
    id_empresa = fields.Many2one('gestionpracticas.empresa', string='Empresa', required=True)
    fecha_inicio = fields.Date(string="Fecha de Inicio", required=True)
    fecha_fin = fields.Date(string="Fecha de Fin", required=True)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fecha_fin_posterior_inicio(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin and record.fecha_fin < record.fecha_inicio:
                raise ValidationError("La fecha del final no puede ser anterior a la fecha de inicio.")

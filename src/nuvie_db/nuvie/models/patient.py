import nuvie_db.nuvie.core as mc

from nuvie_db.nuvie import metadata
from datetime import datetime, date
from sqlmodel import Field, SQLModel
from pydantic import computed_field
from typing import Optional


class PatientBase(mc.BaseModelNuvie_):
    birth_date: Optional[datetime] = Field(
        nullable=False,
        description='Data de nascimento do paciente.',
    )
    death_date: Optional[datetime] = Field(
        nullable=True,
        description='Data de falecimento do paciente. Nulo se o paciente estiver vivo.',
    )
    SSN: str = Field(
        nullable=False,
        unique=True,
        description='Número de Segurança Social (ou CPF no Brasil) do paciente.',
    )
    full_name: Optional[str] = Field(
        nullable=False,
        description='Nome completo do paciente.',
    )
    gender: Optional[str] = Field(
        nullable=True,
        description='Gênero do paciente (ex: Masculino, Feminino, Não Binário).',
    )
    self_declared_color: Optional[str] = Field(
        nullable=True,
        description='Cor/raça autodeclarada pelo paciente (ex: Branco, Preto, Pardo, Amarelo, Indígena).',
    )
    civil_state: Optional[str] = Field(
        nullable=True,
        description='Estado civil do paciente (ex: Solteiro, Casado, Divorciado, Viúvo).',
    )
    income: Optional[float] = Field(
        nullable=True,
        description='Renda mensal ou anual do paciente.',
    )
    address: Optional[str] = Field(
        nullable=True,
        description='Endereço residencial completo do paciente.',
    )
    city: Optional[str] = Field(
        nullable=True,
        description='Cidade de residência do paciente.',
    )
    state: Optional[str] = Field(
        nullable=True,
        description='Estado de residência do paciente.',
    )
    zip_code: Optional[str] = Field(
        nullable=True,
        description='Código postal (CEP no Brasil) do endereço do paciente.',
    )
    phone_number: Optional[str] = Field(
        nullable=True,
        description='Número de telefone de contato do paciente.',
    )
    email: Optional[str] = Field(
        nullable=True,
        description='Endereço de e-mail do paciente.',
    )
    weight_kg: Optional[float] = Field(
        nullable=True,
        description='Peso do paciente em quilogramas.',
    )
    occupation: Optional[str] = Field(
        nullable=True,
        description='Profissão ou ocupação atual do paciente.',
    )
    healthcare_coverage: Optional[str] = Field(
        nullable=True,
        description='Informações sobre a cobertura de plano de saúde do paciente (ex: SUS, Convênio Médico, Nenhum).',
    )


class PatientCreate(SQLModel):
    birth_date: Optional[datetime] = Field(
        nullable=False,
        description='Data de nascimento do paciente.',
    )
    death_date: Optional[datetime] = Field(
        nullable=True,
        description='Data de falecimento do paciente. Nulo se o paciente estiver vivo.',
    )
    SSN: str = Field(
        nullable=False,
        unique=True,
        description='Número de Segurança Social (ou CPF no Brasil) do paciente.',
    )
    full_name: Optional[str] = Field(
        nullable=False,
        description='Nome completo do paciente.',
    )
    gender: Optional[str] = Field(
        nullable=True,
        description='Gênero do paciente (ex: Masculino, Feminino, Não Binário).',
    )
    self_declared_color: Optional[str] = Field(
        nullable=True,
        description='Cor/raça autodeclarada pelo paciente (ex: Branco, Preto, Pardo, Amarelo, Indígena).',
    )
    civil_state: Optional[str] = Field(
        nullable=True,
        description='Estado civil do paciente (ex: Solteiro, Casado, Divorciado, Viúvo).',
    )
    income: Optional[float] = Field(
        nullable=True,
        description='Renda mensal ou anual do paciente.',
    )
    address: Optional[str] = Field(
        nullable=True,
        description='Endereço residencial completo do paciente.',
    )
    city: Optional[str] = Field(
        nullable=True,
        description='Cidade de residência do paciente.',
    )
    state: Optional[str] = Field(
        nullable=True,
        description='Estado de residência do paciente.',
    )
    zip_code: Optional[str] = Field(
        nullable=True,
        description='Código postal (CEP no Brasil) do endereço do paciente.',
    )
    phone_number: Optional[str] = Field(
        nullable=True,
        description='Número de telefone de contato do paciente.',
    )
    email: Optional[str] = Field(
        nullable=True,
        description='Endereço de e-mail do paciente.',
    )
    weight_kg: Optional[float] = Field(
        nullable=True,
        description='Peso do paciente em quilogramas.',
    )
    occupation: Optional[str] = Field(
        nullable=True,
        description='Profissão ou ocupação atual do paciente.',
    )
    healthcare_coverage: Optional[str] = Field(
        nullable=True,
        description='Informações sobre a cobertura de plano de saúde do paciente (ex: SUS, Convênio Médico, Nenhum).',
    )


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase, table=True):
    __tablename__ = metadata.PATIENT_TABLE
    __table_args__ = {'extend_existing': True, 'schema': metadata.SCHEMA_NAME}

    id: str = Field(default=None, primary_key=True)

    @computed_field
    @property
    def age(self) -> Optional[int]:
        if not self.birth_date:
            return None
        try:
            birth = self.birth_date.date()
            today = date.today()
            return (
                today.year
                - birth.year
                - ((today.month, today.day) < (birth.month, birth.day))
            )
        except ValueError:
            return None

    @computed_field
    @property
    def patient_basic_data(self) -> str | None:
        dados = {
            'Nome': self.full_name,
            'Idade': self.age,
            'Peso': self.weight_kg,
            'Gênero': self.gender,
            'Cor/Raça': self.self_declared_color,
        }

        lines = [
            f'{campo}: {valor}'
            for campo, valor in dados.items()
            if valor is not None
        ]
        if not lines:
            return None

        return f'Dados Básicos do Paciente {self.id}: ' + ', '.join(lines)


class PatientPublic(PatientBase):
    id: int


class PatientPublicWithDetails(PatientBase):
    id: int


class PatientsPublic(SQLModel):
    data: list[PatientPublic]
    count: int

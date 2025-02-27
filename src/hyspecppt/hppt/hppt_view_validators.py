import copy

from qtpy.QtCore import QObject
from qtpy.QtGui import QDoubleValidator, QValidator


class AbsValidator(QDoubleValidator):
    """Absolute value validator"""

    def __init__(self, parent: QObject, bottom: float, top: float, decimals: int = -1) -> None:
        """Constructor for the absolute value validator. All the parameters
           are the same as for QDoubleValidator, but the valid value is between a
           positive bottom and top, or between -top and -bottom

        Args:
            parent (QObject): Optional parent
            bottom (float): the minimum positive value (set to 0 if not positive)
            top (float): the highest top value (set to infinity if not greater than bottom)
            decimals (int): the number of digits after the decimal point.

        """
        super().__init__(parent=parent, bottom=bottom, top=top, decimals=decimals)

    def validate(self, inp: str, pos: int) -> tuple[QValidator.State, str, int]:
        """Override for validate method

        Args:
            inp (str): the input string
            pos (int): cursor position

        """
        original_str = copy.copy(inp)
        original_pos = pos
        if inp == "-":
            return QValidator.Intermediate
        try:
            inp = str(abs(float(inp)))
        except ValueError:
            pass
        x = super().validate(inp, pos)
        # do not "fix" the input
        return x[0], original_str, original_pos


class AngleValidator(QValidator):
    """Angle  validator"""

    alpha: QObject
    beta: QObject
    gamma: QObject
    individual: QValidator

    def __init__(self, parent: QObject, alpha: QObject, beta: QObject, gamma: QObject, individual: QValidator) -> None:
        """Constructor for the angle value validator.

        Args:
            parent (QObject): parent
            alpha (float): the alpha field
            beta (float): the beta field
            gamma (float):the gamma field
            individual (QValidator): validator for each field

        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.individual = individual

        super().__init__(parent=parent)

    def validate(self, input_text: str, pos: int) -> tuple[QValidator.State, str, int]:
        """Override for validate method

        Args:
            input_text (str): the input string
            pos (int): cursor position

        """
        # check the individual field value first
        field_validation = self.individual.validate(input_text, pos)
        field_validation_status, field_input, field_pos = field_validation

        # in case this is valid
        if field_validation_status == QValidator.Acceptable:
            alpha_value = self.alpha.text()
            beta_value = self.beta.text()
            gamma_value = self.gamma.text()

            if alpha_value and beta_value and gamma_value:
                alpha_value = float(alpha_value)
                beta_value = float(beta_value)
                gamma_value = float(gamma_value)

                # 1. check all three angles' values are less than 360 degrees
                angle_sum = alpha_value + beta_value + gamma_value
                # 2. check if they can form a triangle.
                alpha_beta_sum = alpha_value + beta_value
                alpha_gamma_sum = alpha_value + gamma_value
                beta_gamma_sum = beta_value + gamma_value

                # check the conditions
                if angle_sum > 360 or (
                    alpha_beta_sum <= gamma_value or alpha_gamma_sum <= beta_value or beta_gamma_sum <= alpha_value
                ):
                    return QValidator.Intermediate, field_input, field_pos
                else:
                    return QValidator.Acceptable, field_input, field_pos
        return field_validation

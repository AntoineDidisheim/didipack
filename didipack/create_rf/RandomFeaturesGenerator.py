import os
import pandas as pd
import numpy as np
from typing import Optional, Tuple
import time




class RandomFeaturesSpecs:
    def __init__(
            self,
            distribution = 'normal',
            distribution_parameters: list =None,
            activation = 'cos_and_sin',
            bias_distribution:str = None,
            bias_distribution_parameters: list =None,
            ranking: bool = True,
            binning_feature: bool = False,
            random_rotation: bool = False
    ):
        # if distribution =='normal':
        #     assert (type(distribution_parameters)==list) & (len(distribution_parameters)==2), \
        #         "For a 'normal' distribution of parameters please define distribution_parameters as a list [mean, std]"
        # if bias_distribution =='normal':
        #     assert (type(bias_distribution_parameters)==list) & (len(bias_distribution_parameters)==2), \
        #         "For a 'normal' distribution of parameters please define distribution_parameters as a list [mean, std]"
        if distribution_parameters is None:
            distribution_parameters = [0,1]

        self.distribution = distribution
        self.distribution_parameters = distribution_parameters
        self.activation = activation
        self.bias_distribution = bias_distribution
        self.bias_distribution_parameters = bias_distribution_parameters
        self.number_features = None
        self.binning_feature = binning_feature
        self.random_rotation = random_rotation
        self.ranking = ranking






class RandomFeaturesGenerator:
    """



    """

    # the next shows the number of basic_parameters defining the distribution
    distribution_requirements = {
        "beta": 2,
        "binomial": 2,
        "chisquare": 0,
        "dirichlet": 1,
        "exponential": 0,
        "f": 2,
        "gamma": 1,
        "geometric": 1,
        "gumbel": 2,
        "hypergeometric": 2,
        "laplace": 2,
        "logistic": 2,
        "lognormal": 2,
        "logseries": 1,
        "multinomial": 2,
        "multivariate_normal": 2,
        "negative_binomial": 2,
        "noncentral_chisquare": 2,
        "noncentral_f": 3,
        "normal": 2,
        "normal_as_old": 2,
        "pareto": 1,
        "poisson": 1,
        "power": 1,
        "rayleigh": 1,
        "standard_cauchy": 0,
        "standard_exponential": 0,
        "standard_gamma": 1,
        "standard_normal": 0,
        "standard_t": 1,
        "triangular": 3,
        "uniform": 2,
        "vonmises": 2,
        "wald": 2,
        "weibull": 1,
        "zipf": 1,
        "gaussian_mixture": 0,
    }

    permitted_activation_functions = [
        "cos",
        "sin",
        "exp",
        "arctan",
        "tanh",
        "ReLu",
        "Elu",
        "SoftPlus",
        "cos_and_sin",
    ]


    def __init__(
            self,
            build_factor: bool = True,
            rf_spec_list: [list, RandomFeaturesSpecs] = RandomFeaturesSpecs(),
            compute_instrument_quantities: object = False,
            half_linear_features: bool = False

    ):
        if type(rf_spec_list) == RandomFeaturesSpecs:
            rf_spec_list = [rf_spec_list]

        self.build_factors = build_factor
        self.rf_spec_list = rf_spec_list
        self.compute_instrument_quantities = compute_instrument_quantities
        self.half_linear_features = half_linear_features



    def generate_random_features_from_list_with_potential_ranking(
            self,
            seed: int,
            batch_nb_rf: int,
            date_ids: np.ndarray,
            x_mat: np.ndarray,
            y_mat: [np.ndarray, None] = None,
            permute_randomly: bool = False,
    ) -> pd.DataFrame:

        """
        This is a key function for generating random features, with the possibility to cross-sectionally rank them
        If msrr or factor_msrr, then we will actually multiply signals * returns
        Parameters
        ----------
        seed :
        compute_instrument_quantities: if true, we are NOT going to produce the random factors or even feature,
        only use random signals to compute buidling blocks of pricing errors
        msrr :
        factor_msrr: if true, then we actually build factors
        batch_nb_rf : number random features
        pre_specified_list_of_specs_for_random_features :
        date_ids: We use then to groupby when we build factors
        y_mat: (NT) \times 1 panel of stock returns
        x_mat :

        Returns
        -------
        first we generate random_features: (NT) \times (number_features_in_subset)
        matrix: array of random features for the panel of
        N stocks and T dates

        If factor_msrr = True, we return (T \times number_features_in_subset) because we groupby dates !
        If factor_msrr = False, then we return original size  (NT) \times (number_features_in_subset)


        """

        # we define here the number of random features per group.
        size_per_group = int(np.floor(batch_nb_rf/len(self.rf_spec_list)))
        left_over = int(batch_nb_rf-size_per_group*len(self.rf_spec_list))
        for i in range(len(self.rf_spec_list)):
            if i == len(self.rf_spec_list)-1:
                self.rf_spec_list[i].number_features = size_per_group+left_over
            else:
                self.rf_spec_list[i].number_features = size_per_group


        random_features_for_generation = []
        for spec in self.rf_spec_list:
            random_features_for_generation.append(
                self._generate_random_features_from_spec(
                    seed=seed,
                    spec=spec,
                    x_mat=x_mat,
                    date_ids=date_ids
                )
            )
        random_features_for_generation = np.concatenate(random_features_for_generation,axis=1)

        if self.build_factors:
            # note that we update the dates according to the groupby so that we can get the updated dates as output
            random_features_for_generation = self._build_random_factors(x_mat=random_features_for_generation, y_mat=y_mat, dates_ids=date_ids)
        else:
            random_features_for_generation = pd.DataFrame(random_features_for_generation,index=date_ids.flatten())
        random_features_for_generation.index.name = 'date'


        if permute_randomly:
            perm = np.random.permutation(random_features_for_generation.shape[1])
            random_features_for_generation = random_features_for_generation.loc[:, perm]

        return random_features_for_generation

    def _rank_features_cross_sectionally(self,
                                         unkranked_x: np.ndarray,
                                         date_ids: np.ndarray,
                                         print_time: bool = False):
        """
        Ranking features on each date. This is done in numpy for speed, but the drawback is that
        we assume dates are pre-ordered
        Parameters
        ----------
        unkranked_x
        date_ids
        ranking
        axis_
        print_time : If true we print the run tiem
        use_pands :  IF true we run the pandas version.

        Returns
        -------

        """

        date_ids = np.array(date_ids)

        """
        Important: the code assumes that date_ids are already sorted! 
        Pre-process the data so that date_ids are increasing !! 
        """
        # here it is important that dates are sorted because when we concatenate,
        # we do so in the order of dates
        start = time.time()
        ranked_signals = pd.DataFrame(unkranked_x)
        if len(date_ids.shape)==2:
            date_ids = date_ids.flatten()
        ranked_signals = ranked_signals.groupby(date_ids).rank(pct=True, axis=0) - 0.5
        ranked_signals = ranked_signals.values
        if print_time:
            print('Time pandas', time.time() - start)

        ranked_signals[np.isnan(unkranked_x)] = np.nan

        return ranked_signals

    @staticmethod
    def _check_distribution_requirements(
            distribution: str,
            distribution_parameters: list
    ):

        if distribution == "gaussian_mixture":
            return
        if distribution not in RandomFeaturesGenerator.distribution_requirements:
            raise Exception(
                f"{distribution} is not permitted. If you need it, do not be lazy and update the class"
            )
        elif (
                len(distribution_parameters)
                != RandomFeaturesGenerator.distribution_requirements[distribution]
        ):
            raise Exception(
                f"{distribution} "
                f"requires {RandomFeaturesGenerator.distribution_requirements[distribution]} basic_parameters"
            )


    def _build_random_factors(
            self,
            x_mat,
            y_mat: np.ndarray,
            dates_ids: np.ndarray) -> pd.DataFrame:
        """

        Parameters
        ----------
        x_mat: (NT) \times (number_features_in_subset)  matrix: array of random features for the panel of
        N stocks and T dates
        y_train: (NT) \times 1 panel of stock returns
        factor_msrr: if true, then we actually build factors
        dates_ids: dates. We use then to groupby when we build factors

        Returns
        -------
        If factor_msrr = True, we return (T \times number_features_in_subset) because we groupby dates !
        If factor_msrr = False, then we return original size  (NT) \times (number_features_in_subset)

        """
        x_mat = x_mat * y_mat.reshape(-1, 1)  # these are actually managed returns, R * F(S)
        if type(x_mat) == np.ndarray:
            x_mat = pd.DataFrame(x_mat)
        if len(dates_ids.shape)== 2:
            dates_ids = dates_ids.flatten()
        x_mat = x_mat.groupby(dates_ids).mean()
        return x_mat

    def _generate_random_features_from_spec(
            self,
            x_mat: np.ndarray,
            spec: RandomFeaturesSpecs,
            date_ids: np.ndarray,
            seed: int = None
    ) -> np.ndarray:

        """
        The starting points
        given a list of different specifications, generate random features for each of them
        normally, it should receive specifications as pre_specified_list_of_specs
        but if not, then we give specification details explicitly
        Parameters
        ----------
        number_features_in_subset: number of features per gamma
        x_mat: actual raw features
        reproducible, yet each chuck must yield new features. increment_seed takes care of it
        single_precision: this is for memory saving and gpu
        pre_specified_list_of_specs: the main thing: a list specifying all details of random features
        seed: random seed

        Returns
        -------

        """
        np.random.seed(seed)
        if spec.binning_feature:
            random_features_for_spec = self._generate_random_binning_features(x_mat=x_mat, spec=spec, seed=seed)
        else:
            random_features_for_spec = self.generate_random_neuron_features(x_mat=x_mat, spec=spec,seed=seed)

        if spec.ranking:
            random_features_for_spec = self._rank_features_cross_sectionally(
                unkranked_x= random_features_for_spec,
                date_ids=date_ids,
            )

        return random_features_for_spec


    @staticmethod
    def _apply_activation_to_multiplied_signals(
            multiplied_signals,
            activation: str
    ) -> np.ndarray:
        """
        this method takes as input signaled already multipled by some weights + cosntant: w*x+b
        and returns act(w*x+b)
        :rtype: object
        """
        if activation in ["cos", "sin", "exp", "arctan", "tanh"]:
            final_random_features = getattr(np, activation)(multiplied_signals)
        elif activation == "cos_and_sin":
            final_random_features = np.concatenate(
                [np.cos(multiplied_signals), np.sin(multiplied_signals)], axis=0
            )

        elif isinstance(activation, str) and activation.lower() == "relu":
            final_random_features = multiplied_signals * (multiplied_signals > 0)
        elif isinstance(activation, list) and activation[0].lower() == "elu":
            final_random_features = (
                                            multiplied_signals * (multiplied_signals > 0)
                                    ) + activation[1] * (np.exp(multiplied_signals) - 1) * (
                                            multiplied_signals < 0
                                    )
        elif activation.lower() == "softplus":
            final_random_features = np.log(1 + np.exp(multiplied_signals))
        elif activation.lower() == "linear":

            final_random_features = multiplied_signals
        else:
            raise Exception(f"activation function={activation} is not yet supported")
        return final_random_features

    def _add_bias(
            self,
            multiplied_signals,
            bias_distribution,
            bias_distribution_parameters,
            seed=0,
    ):
        """
        Careful, multiplied signals are assumed to be P \times n where P is the sumber of signals
        and n the number of observations
        Parameters
        ----------
        multiplied_signals :
        bias_distribution :
        bias_distribution_parameters :
        Returns
        -------
        """
        np.random.seed(seed)
        number_features = multiplied_signals.shape[0]
        random_bias = getattr(np.random, bias_distribution)(
            *bias_distribution_parameters, [number_features, 1]
        )
        # here we are using numpy broadcasting to add the same bias every time period
        multiplied_signals += random_bias
        return multiplied_signals

    def generate_random_neuron_features(
            self,
            x_mat: np.ndarray,
            seed: int,
            spec : RandomFeaturesSpecs
    ) -> np.ndarray:

        """

        this function builds random neuron features f(w'S+bias) where w is
        a vector of random weights and f is an activation function, and bias is a random bias

        One important special case is a gaussian mixture, whereby we generate random scales (gamma) from the interval
        [gamma_min, gamma_max], uniformly

        :param distribution_parameters:
        :param distribution:
        :param activation:
        :param number_features:
        :param bias_distribution:
        :param gamma_method: random or linear to randomly draw it or get a grid
        :param gama_param: if not none we use gamma and we draw it from x to y -> [x,y]
        :return:
        """
        np.random.seed(seed)
        signals = x_mat

        RandomFeaturesGenerator._check_distribution_requirements(
            spec.distribution, spec.distribution_parameters
        )
        if spec.bias_distribution:
            RandomFeaturesGenerator._check_distribution_requirements(
                spec.bias_distribution,
                spec.bias_distribution_parameters,
            )

        number_signals = signals.shape[1]
        size = [number_signals, spec.number_features]
        if spec.activation == "cos_and_sin":
            size = [number_signals, int(spec.number_features / 2)]
        # first we initialize the random seed

        # X = np.random.normal(0, a) means X is distributed as Normal(0, a^2).  (a=standard deviation)
        # This is an important property of Gaussian distributions: multiplying by a constant keeps is Gaussian,
        # just scales the standard deviation
        if spec.distribution != "gaussian_mixture":
            random_vectors = getattr(np.random, spec.distribution)(*spec.distribution_parameters, size)
        else:
            random_vectors = getattr(np.random, "standard_normal")(size)
            gamma_values = spec.distribution_parameters
            minimal_gamma = gamma_values[0]
            maximal_gamma = gamma_values[1]
            all_gamma_values = np.random.uniform(minimal_gamma, maximal_gamma, [1, size[1]])
            # now we use numpy broadcasting to do elemen-wise multiplication.
            random_vectors = random_vectors * all_gamma_values

        # w'x, where w is our random vector
        multiplied_signals = np.matmul(random_vectors.T, signals.T)
        if spec.bias_distribution:
            multiplied_signals = RandomFeaturesGenerator._add_bias(
                multiplied_signals, spec.bias_distribution, spec.bias_distribution_parameters
            )
        final_random_features = (
            RandomFeaturesGenerator._apply_activation_to_multiplied_signals(
                multiplied_signals, spec.activation
            )
        )

        return final_random_features.T

    @staticmethod
    def _generate_random_binning_features(x_mat: np.ndarray,
                                          spec:RandomFeaturesSpecs,
                                          random_seed=0,
                                          seed=0):
        """
           WARNING: THE FEATURES ARE SUPPOSED TO BE NORMALIZED!!!
           ALWAYS PRE-PROCESS THE DATA (USING ROLLING WINDOW) !!!
           signals are assumed to be T \times M
           :param random_seed:
           :param random_rotation:
           :param distribution_parameters:
           :param distribution:
           :param distribution_requirements:
           :param x_mat:
           :param number_features:
           :return:
           """
        np.random.seed(seed)
        RandomFeaturesGenerator._check_distribution_requirements(spec.distribution,
                                                                 spec.distribution_parameters)

        number_signals = x_mat.shape[1]
        size = [number_signals, spec.number_features]
        np.random.seed(random_seed)
        if spec.random_rotation:
            rotate = np.random.randn(x_mat.shape[1], x_mat.shape[1])
            tmp = np.matmul(rotate, rotate.T)
            _, eigvec = np.linalg.eigh(tmp)
            # now, eigenvectors give a random rotation
            signals_rotated = np.matmul(eigvec.T, x_mat.T).T
        else:
            signals_rotated = x_mat.copy()
        delta = getattr(np.random, spec.distribution)(*spec.distribution_parameters, size)
        delta = delta * (np.abs(delta) > (10 ** (- 10))) + (np.abs(delta) < (10 ** (- 10))) * (10 ** (-10))  # clip
        u_ = np.random.uniform(0, 1, [number_signals, spec.number_features]) * delta
        subtracted = signals_rotated.reshape(x_mat.shape[0], 1, number_signals) \
                     - u_.reshape(1, spec.number_features, number_signals)
        subtracted_and_divided = subtracted / delta.reshape(1, spec.number_features, number_signals)

        binned_signals = np.floor(subtracted_and_divided).reshape([x_mat.shape[0],
                                                                   x_mat.shape[1] * spec.number_features])
        return binned_signals

    @staticmethod
    def _generate_a_random_covariance_matrix_with_given_eigenvalues(
            eigenvalues: np.ndarray, seed=0
    ) -> np.ndarray:
        """

        Parameters
        ----------
        eigenvalues :

        Returns
        -------
        a random matrix with prescribed eigenvalues
        """
        eigenvalues = eigenvalues.flatten()
        size = len(eigenvalues)
        random_shocks = np.random.normal(size=[size, 2 * size])
        sigma = random_shocks @ random_shocks.T
        _, eigenvectors = np.linalg.eigh(sigma)
        # t1 = time.time()
        # eigenvectors = ortho_group.rvs(size, random_state=seed)
        # matrix = eigenvectors @ (np.diag(eigenvalues) @ eigenvectors.T)
        # t2 = time.time()
        # print(f'got the random O matrix in {t2 - t1}')
        matrix = eigenvectors @ (np.diag(eigenvalues) @ eigenvectors.T)
        return matrix




if __name__ == "__main__":
    pass
    # c_sigma = 3.0
    # list_of_widths = [300, 300, 600]
    #
    # X_train = np.random.normal(size=(100, 100))

    # distribution = "gaussian_mixture"
    # gamma = [1.0, 1.0]
    # activation = "relu"
    #
    # random_features = RandomFeaturesGenerator.generate_random_deep_neuron_features(
    #     c_sigma, list_of_widths, X_train, distribution, gamma, activation
    # )





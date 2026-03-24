function [results, obj_val,generator_vals] = custom_dcopf(case_name,type_of_min,which_health_fcn)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
% if carbon_cost = True, will run carbon optimization based on economic
% cost of carbon
% INPUTS:
%   case_name: string with the casefile name ie 'Fall116Generous'
%   type_of_min: the type of minimization/optimization you want to run. the
%   Options are: 
%   - "carbon" for a carbon emissions minimization
%   - "mix estimate" for a health cost made up of a linear combination of
%   the three health costs (carbon cost, health cost, and economic cost)
%   - "low estimate" for a health cost minimzation with the lower bound
%   coefficients
%   - "high estimate" for a health cost with the upper bound coefficients
%   which_health_fcn: options are "low" and "high", for which upper bound
%   you want to use when running a mixed health cost optimization

%% 1. Load case
    % mpc = loadcase('Fall116Generous');   % replace with your case file
    mpc = loadcase(case_name);

    % set carbon cost to false so that it runs the carbon optimizatio with
    % emissions amounts instead of cost amounts, shouldn't make a
    % difference
    carbon_cost = false;
    
    %% 2. Save original costs
    orig_gencost = mpc.gencost;   % full backup

     
    % disp(orig_gencost);
    high_estimate_costs = [0.000000000000000000e+00;5.374672901722723140e+01;7.246656191291578401e-07;0.000000000000000000e+00;0.000000000000000000e+00;1.169190877666764550e+01;0.000000000000000000e+00;7.348003919583820043e+00;0.000000000000000000e+00;2.542076053944515024e+03;9.431391249592208226e+01;0.000000000000000000e+00;1.468668175233070201e+02;0.000000000000000000e+00;5.060653736886130361e+01;1.171227524182394745e+03;4.100082128042653267e+02;1.198595841790736785e+02;1.198595279142268026e+02;1.198595550526913200e+02;1.209862509929198779e+02;9.431390831864381141e+01;1.305604286454129408e+02;9.200488314461722439e+01;6.529686932203776273e+00;2.969645379289908682e+00;2.902121261470498315e+00;4.653661864536261987e+02;8.309683436589203609e+01;1.176945412868455833e+03;1.033338688267716208e+02;1.033337276233113045e+02;0.000000000000000000e+00;1.139190729568042286e+02;8.812035421713601124e+01;1.139191188086145843e+02;1.758232368409921094e+02;3.725641543621768648e+01;0.000000000000000000e+00;3.887820448053059863e+01;1.169192357828745621e+01;1.169190709706035136e+01];
    
    low_estimate_costs= [0.000000000000000000e+00;3.986551108233063445e+01;8.297763289472955791e-07;0.000000000000000000e+00;0.000000000000000000e+00;9.173699787088585467e+00;0.000000000000000000e+00;5.326068296491544451e+00;0.000000000000000000e+00;1.803977128617686503e+03;7.087318865967262127e+01;0.000000000000000000e+00;8.713235489303770009e+01;0.000000000000000000e+00;2.977542623445600256e+01;8.733223270358625996e+02;2.905190461379883686e+02;8.999394944427116627e+01;8.999389713638589683e+01;8.999392266826922082e+01;8.819176030838676184e+01;7.087318509280464696e+01;9.620594490670536914e+01;7.124231053328479391e+01;4.869667357602610380e+00;2.248393022858907742e+00;2.170614480160758308e+00;3.304958770075545544e+02;4.848494628896055048e+01;9.020057872755376138e+02;6.455866331908775635e+01;6.455853305633793582e+01;0.000000000000000000e+00;7.159856160293067262e+01;5.050325265306687328e+01;7.159860748392492269e+01;1.164360843566790749e+02;2.891185543812598624e+01;0.000000000000000000e+00;3.076989355201919452e+01;9.173712714069887753e+00;9.173698414433641091e+00];    
    
    % Start of Running Carbon Cost!!!
    carbon_emissions = [0.000000000000000000e+00;4.849999999999999867e-01;4.849999999999999867e-01;0.000000000000000000e+00;0.000000000000000000e+00;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;1.229999999999999982e+00;4.849999999999999867e-01;0.000000000000000000e+00;4.849999999999999867e-01;0.000000000000000000e+00;4.849999999999999867e-01;1.229999999999999982e+00;1.229999999999999982e+00;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;1.229999999999999982e+00;4.849999999999999867e-01;1.229999999999999982e+00;4.849999999999999867e-01;4.849999999999999867e-01;0.000000000000000000e+00;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01;0.000000000000000000e+00;4.849999999999999867e-01;0.000000000000000000e+00;4.849999999999999867e-01;4.849999999999999867e-01;4.849999999999999867e-01];
    
    % carbon_costs = [0.000000000000000000e+00;8.142014519056259303e+01;8.142014519056259303e+01;0.000000000000000000e+00;0.000000000000000000e+00;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;2.064882032667876217e+02;8.142014519056259303e+01;0.000000000000000000e+00;8.142014519056259303e+01;0.000000000000000000e+00;8.142014519056259303e+01;2.064882032667876217e+02;2.064882032667876217e+02;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;2.064882032667876217e+02;8.142014519056259303e+01;2.064882032667876217e+02;8.142014519056259303e+01;8.142014519056259303e+01;0.000000000000000000e+00;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01;0.000000000000000000e+00;8.142014519056259303e+01;0.000000000000000000e+00;8.142014519056259303e+01;8.142014519056259303e+01;8.142014519056259303e+01];

    cost_of_carbon = 167.83;
    % if (type_of_min == "original")
    %     results = rundcopf(mpc);
    % end
    if(type_of_min == "carbon" && carbon_cost == false)
        disp('minimizing carbon emissions')
        % change cost back to origional
        mpc.gencost = orig_gencost;
        % Carbono only emissions 
        for g = 1:size(mpc.gencost, 1)
            mpc.gencost(g, 7) = carbon_emissions(g);
            mpc.gencost(g,6) = 0;
            mpc.gencost(g,8) = 0;
        end
        disp('ran carbon costs')
    end

    if(type_of_min == "mix estimate" && which_health_fcn == "high")
        disp('minimizing mix of cost functions w high est health cost')
        % change cost back to origional
        mpc.gencost = orig_gencost;
        % Carbono only emissions 
        for g = 1:size(mpc.gencost, 1)
            mpc.gencost(g, 7) = mpc.gencost(g,7) + cost_of_carbon*carbon_emissions(g) + high_estimate_costs(g);
            % mpc.gencost(g,6) = 0;
            % mpc.gencost(g,8) = 0;
        end
        disp('ran mix estiamte costs w high est health cost')
    end

    if(type_of_min == "mix estimate" && which_health_fcn == "low")
        disp('minimizing mix of cost functions w high est health cost')
        % change cost back to origional
        mpc.gencost = orig_gencost;
        % Carbono only emissions 
        for g = 1:size(mpc.gencost, 1)
            mpc.gencost(g, 7) = mpc.gencost(g,7) + cost_of_carbon*carbon_emissions(g) + low_estimate_costs(g);
            % mpc.gencost(g,6) = 0;
            % mpc.gencost(g,8) = 0;
        end
        disp('ran mix estimate costs w low est health costs')
    end


    if(type_of_min == "carbon" && carbon_cost == true)
        disp('minimizing cost of carbon)')
        % change cost back to origional
        mpc.gencost = orig_gencost;
        % Carbono only emissions 
        for g = 1:size(mpc.gencost, 1)
            mpc.gencost(g, 7) = carbon_emissions(g)*203.928;
            mpc.gencost(g,6) = 0;
            mpc.gencost(g,8) = 0;
        end
    end

    if(type_of_min == "low estimate")
        disp('minimize low estimate')
        for g = 1:size(mpc.gencost, 1)
            mpc.gencost(g, 7) = low_estimate_costs(g);
            mpc.gencost(g,6) = 0;
            mpc.gencost(g,8) = 0;
        end
        disp(mpc.gencost);
    end

    if(type_of_min == "high estimate")
        disp('minimize high estimate')
        for g = 1:size(mpc.gencost, 1)
            mpc.gencost(g, 7) = high_estimate_costs(g);
            mpc.gencost(g,6) = 0;
            mpc.gencost(g,8) = 0;
        end
        disp(mpc.gencost);
    end


    results = rundcopf(mpc);
    generator_vals = results.gen(:, 2);
    obj_val = results.f;

    % change cost back to origional
    mpc.gencost = orig_gencost;


end